import requests 
import shutil 

#### ADD A 'if r.status_code == 200' #######

class Youtube():

    API_KEY = 'AIzaSyBgVeAZAHJxEA2A4QlxUql7sTTmuWAvotM'
    BASE_URL = 'https://www.googleapis.com/youtube/v3/'

    def __init__(self):
        pass 

    @classmethod 
    def get_upload_id(cls, channel_name):

        channel_name='PewDiePie' 

        data = requests.get(cls.BASE_URL + 
                'channels?part=contentDetails&forUsername={}&key={}'.format(channel_name, cls.API_KEY))

        data_dict = data.json() 
        
        upload_id = data_dict['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return upload_id

    @classmethod
    def get_upload_dict(cls, upload_id, size):
        ''' returns an upload dictionary of a channel based on the uploads id
        of the channel, can specify size as well '''

        upload_data = requests.get(cls.BASE_URL + 
                'playlistItems?part=snippet&maxResults={}&playlistId={}&key={}'.format(size ,upload_id, cls.API_KEY))
        upload_dict = upload_data.json() 
        return upload_dict 
    
    @staticmethod
    def get_upload_titles(upload_dict):
        upload_titles = []  

        for video in upload_dict['items']:
            upload_titles.append(video['snippet']['title'])

        return upload_titles 
    
    @staticmethod
    def get_thumbnails_medium(upload_dict, file_paths=None):
        ''' downloads all the thumbnails from the given playlist dictionary and
        returns their filepaths in an array '''
        
        if file_paths == None:
            file_paths = list('abcdefghijklmnopqrstuvwxyz')
        
        path_counter = 0
        for video in upload_dict['items']:
            thumbnail_url = video['snippet']['thumbnails']['medium']['url']
            thumbnail_data = requests.get(thumbnail_url, stream=True) 
            
            with open(file_paths[path_counter] + '.jpg', 'wb') as f:
                thumbnail_data.raw.decode_content = True
                shutil.copyfileobj(thumbnail_data.raw, f) 

            path_counter += 1
        
        return file_paths[:path_counter] 
            
    def get_upload_times(upload_dict):
        ''' returns the upload times of the videos in an upload dict from
        newest to oldest in an array in YY-MM-DDTh:m format '''

        upload_times = []
        
        for video in upload_dict['items']:
            time_string = video['snippet']['publishedAt']
            last_colon = time_string.rfind(':') 
            time_string = time_string[:last_colon] 
            upload_times.append(time_string)

        return upload_times

    def get_descriptions(upload_dict):
        ''' returns descriptions of videos in an upload dict from newest to
        oldest in an array '''
        descriptions = []

        for video in upload_dict['items']:
            description = video['snippet']['description'] 
            descriptions.append(description) 

        return descriptions 

class Channel():

    def __init__(self, channel_name, return_size=5):
        ''' initializes a Channel object when given a channel name. Can
        optionally specify a return_size that determines how many videos of the
        channel are returned '''

        self.channel_name = channel_name 
        self.return_size = return_size 
        
        self.upload_id = Youtube.get_upload_id(self.channel_name) 
        self.upload_dict = Youtube.get_upload_dict(self.upload_id,
                self.return_size)

    def get_upload_titles(self):
        return Youtube.get_upload_titles(self.upload_dict) 

    def get_thumbnails(self):
        return Youtube.get_thumbnails_medium(self.upload_dict) 

    def get_upload_times(self):
        return Youtube.get_upload_times(self.upload_dict) 

    def get_descriptions(self):
        return Youtube.get_descriptions(self.upload_dict) 


if __name__ == '__main__':
   pewdiepie = Channel('Pewdiepie', return_size=10) 

   print('\n-------------- Upload Titles: --------------') 
   print(pewdiepie.get_upload_titles())
   print('\n-------------- Thumbnail Paths: -------------') 
   print(pewdiepie.get_thumbnails()) 
   print('\n-------------- Upload Times: ----------------') 
   print(pewdiepie.get_upload_times())
   print('\n--------------- Descriptions: ----------------') 
   print(pewdiepie.get_descriptions()) 










































