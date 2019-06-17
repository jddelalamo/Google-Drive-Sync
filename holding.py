LOCAL_TARGET_DIR = '/Users/jd/Desktop/Google-Drive-Sync/testing/recursive test'
RECURSIVE_TEST_FOLDER_ID = '1_Yn8jD-J19paY3ja8DZh8n2KEcrcbin_'
SHARPENING_BUSINESS = '142nFxTXs3O507kBH9fSRG0aUrpXtnpay'
SLASH = '/'

SCOPES = ['https://www.googleapis.com/auth/drive']

store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
	creds = tools.run_flow(flow, store)

DRIVE = build('drive', 'v3', http=creds.authorize(Http()))