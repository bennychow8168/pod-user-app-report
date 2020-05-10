import logging, csv
from sym_api_client_python.configure.configure import SymConfig
from sym_api_client_python.auth.rsa_auth import SymBotRSAAuth
from sym_api_client_python.clients.sym_bot_client import SymBotClient
from sym_api_client_python.clients.admin_client import AdminClient


def configure_logging():
    logging.basicConfig(
            filename='./logs/output.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filemode='w', level=logging.DEBUG
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def main():
    print('Python Client runs using RSA authentication')

    # Configure log
    configure_logging()

    # RSA Auth flow: pass path to rsa config.json file
    configure = SymConfig('./resources/config.json')
    configure.load_config()
    auth = SymBotRSAAuth(configure)
    print('Start Authenticating..')
    logging.info('Start Authenticating..')
    auth.authenticate()

    # Initialize SymBotClient with auth and configure objects
    bot_client = SymBotClient(auth, configure)
    admin_client = AdminClient(bot_client)

    # Retrieve list of users
    print('Retrieve All Active Pod Users...')
    logging.info('Retrieve All Active Pod Users...')

    user_lists = retrieve_all_active_pod_users(admin_client)

    print(f'Retrieved {str(len(user_lists))} users')
    logging.info(f'Retrieved {str(len(user_lists))} users')

    app_list = dict()
    # Loop users and get App
    for user in user_lists:
        print(f'Getting Apps for {user["userAttributes"]["emailAddress"]}')
        logging.info(f'Getting Apps for {user["userAttributes"]["emailAddress"]}')

        install_app = retrieve_installed_apps(bot_client, user["userSystemInfo"]["id"])

        for app in install_app:
            app_id = f"{app['appName']} ({app['appId']})"
            if app_id not in app_list:
                app_list[app_id] = []

            u = dict()
            u['userAttributes'] = user["userAttributes"]
            if 'products' in app and app['products'] is not None:
                u['subscription'] = app['products'][0]['name']
            app_list[app_id].append(u)

    # Print final result
    print(f'Generating Result Files...')
    logging.info(f'Generating Result Files...')
    print_result(app_list)


def print_result(app_list):
    for app_id, user_list in app_list.items():
        file_name = app_id + ".csv"

        with open(file_name, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['User Name',
                          'First Name',
                          'Last Name',
                          'Email',
                          'App Subscription']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for u in user_list:
                writer.writerow(
                        {'User Name': u['userAttributes']['userName'],
                         'First Name': u['userAttributes']['firstName'],
                         'Last Name': u['userAttributes']['lastName'],
                         'Email': u['userAttributes']['emailAddress'],
                         'App Subscription': u['subscription'] if 'subscription' in u else ''})

    return


def retrieve_all_active_pod_users(admin_client):
    output = admin_client.admin_list_users(skip=0, limit=1000)

    while True:
        next_out = admin_client.admin_list_users(skip=int(len(output)), limit=1000)
        if len(next_out) > 0:
            for index in range(len(next_out)): output.append(next_out[index])
        else:
            break

    # Filter out Service Acc and Disabled users
    final_result = []
    for u in output:
        if u["userAttributes"]["accountType"] == "NORMAL" and u["userSystemInfo"]["status"] == "ENABLED":
            final_result.append(u)

    return final_result


def retrieve_installed_apps(bot_client, user_id):
    output = admin_get_user_features(bot_client, user_id)

    # Filter install apps only
    final_result = []
    for o in output:
        if o["install"]:
            if 'products' in o and o['products'] is not None:
                new_prod = []
                for p in o['products']:
                    if p['subscribed']:
                        new_prod.append(p)
                o['products'] = new_prod
            final_result.append(o)

    return final_result


def admin_get_user_features(bot_client, user_id):
        url = '/pod/v1/admin/user/{0}/app/entitlement/list'.format(user_id)
        return bot_client.execute_rest_call("GET", url)


if __name__ == "__main__":
    main()