import geoip2.database
from user_agents import parse

from app.db.models import ShortLinkDetails


async def collect_short_link_details(short_key, request_obj, maxmind_db_path, db_session):
    # getting IP address data from maxmind db
    ip_address = request_obj.client.host
    with geoip2.database.Reader(maxmind_db_path) as reader:
        try:
            location_data = None
            response = reader.city(ip_address)                          # Only public address can be found in maxmind_db
            location_data = {
                "city": response.city.name,
                "region": response.subdivisions.most_specific.name,
                "country": response.country.name,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
                "postal_code": response.postal.code,
                "continent": response.continent.name,
                "timezone": response.location.time_zone
            }

        except geoip2.errors.AddressNotFoundError:
            print({"error": "IP address not found in the database."})

        finally:
            # getting and Parsing the user agent data
            user_agent = request_obj.headers.get('user-agent')
            parsed_user_agent = parse(user_agent)
            user_agent_list = str(parsed_user_agent).split(' / ')

            device =  'PC' if user_agent_list[0] == "PC" else 'MOBILE'
            os = user_agent_list[1]
            browser = user_agent_list[2]
            country = location_data.get('country', None) if location_data else None
            city = location_data.get('city', None) if location_data else None

            short_link_details_obj = ShortLinkDetails(short_key = short_key, device = device, client_ip = ip_address, 
                                    country = country, 	city = city, browsers = browser, OS = os)
            db_session.add(short_link_details_obj)
            db_session.commit()
        