results = self.service.files().list(
            q="properties has {key='udsRoot' and value='true'} and trashed=false",
            pageSize=1,
            fields="nextPageToken, files(id, name, properties)").execute()
        folders = results.get('files', [])