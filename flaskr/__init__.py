import asyncio
import os
import aiohttp
from aiohttp import ClientSession
from flask import Flask, jsonify, request, abort
from space_objects.flaskr.utils import MaxDaysRangeError, date_ranges, parse_neos, valid_date_query_param


def create_app():
    '''Application factory function providing us with Flask application instance'''
    app = Flask(__name__, instance_relative_config=True)
    app.config['API_KEY'] = os.environ.get('API_KEY',default=None)
    if(app.config.get('API_KEY') is None):
        try:
            app.config.from_pyfile('config.py')
        except FileNotFoundError:
        # API_KEY not specified nor in env, then raise ValueError
            raise ValueError('API_KEY env variable not found in config.py file nor in actual environment')
 
    @app.errorhandler(400)
    def bad_request(err):
        return jsonify(error=str(err)), 400

    @app.route('/objects', methods=['GET'])
    async def objects():
        '''
        Returns NEOs for given days range sorted by their closest approach distance to the Earth 
        '''
        neows_url = "https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}"
        start_date, end_date = request.args.get(
            'start_date'), request.args.get('end_date')

        # handle missing query string or exceeded range for days span
        if not valid_date_query_param(start_date) or not valid_date_query_param(end_date):
            abort(400, description='Invalid value for query parameters')
        try:
            date_pairs = date_ranges(start_date, end_date)  # type: ignore
        except MaxDaysRangeError:
            abort(400, description='Maximum range between start and end date exceeded')
        tasks, results, neos = [], [], []

        # make actual request to nasa api
        async with ClientSession() as sess:
            for start, end in date_pairs:
                tasks.append(sess.request(method="GET", url=neows_url.format(
                    start_date=start, end_date=end, api_key=app.config['API_KEY']), timeout=120))
            results = await asyncio.gather(*tasks)
            for res in results:
                try:
                    res.raise_for_status()
                    res_json = await res.json(content_type=None)
                    neos += parse_neos(res_json)
                except aiohttp.ClientError as err:
                    # RequestException should handle HTTPErrors (invalid api_key etc)
                    # These prints should be used as some form of logging mechanism for finding and analyzing occured error
                    print(res.text)
                    print(err)
                    abort(500, "Internal server error")
                except KeyError as err:
                    # These prints should be used as some form of logging mechanism for finding and analyzing occured error in nasa api schema
                    print('KeyError when parsing data from nasa api endpoint - ', err)
                    abort(500, "Internal server error")
                except Exception as err:
                    # Unexpected exception (e.g. timeout)
                    # These print should be used as some form of logging mechanism for finding and analyzing occured error
                    print(err)
                    abort(500, "Internal server error")
        try:
            neos.sort(
                key=lambda neo: neo['close_approach_miss_distance']['astronomical'])
        except KeyError as err:
            # These prints should be used as some form of logging mechanism for finding and analyzing occured error in nasa api schema
            print('KeyError when sorting data from nasa api endpoint - ', err)
            abort(500, "Internal server error")
        return neos

    return app
