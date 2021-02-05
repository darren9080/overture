import os
import io
import pytube
import pandas as pd
from google.cloud import videointelligence
from google.protobuf.json_format import MessageToDict
from urllib.error import HTTPError


class VideoAnalysis:
    def __init__(self):
        credential_path = "C:\\S-Core\\KEYFILE.json"
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
        self.filepath = 'C:\\S-Core\\data\\video\\'

    def download_video(self, url, title):
        '''

        :param url:
        :param title:
        :return:
        '''
        print(title)

        yt = pytube.YouTube(url)
        stream = yt.streams.first()

        try:
            stream.download(self.filepath, title)
        except HTTPError:
            pass

        try:
            stream.download(self.filepath, title)
        except KeyError:
            pass

        stream.download(self.filepath, title)

        file_dir = stream.download(self.filepath, title)
        file_name = file_dir.split("\\", 4)[4].split(".", 1)[0]

        return file_dir, file_name

    def analyze_video(self, file_dir, file_name):
        '''

        :param file_dir:
        :param file_name:
        :return:
        '''
        shot_final = pd.DataFrame()
        seg_final = pd.DataFrame()

        video_client = videointelligence.VideoIntelligenceServiceClient()
        features = [videointelligence.enums.Feature.LABEL_DETECTION]

        with io.open(file_dir, 'rb') as movie:
            input_content = movie.read()

        operation = video_client.annotate_video(features=features, input_content=input_content)
        print('\nProcessing video for label annotations:')

        result = operation.result(timeout=90)
        print('\nFinished processing.')

        serialized = MessageToDict(result)

        seg_label_list = serialized["annotationResults"][0]["segmentLabelAnnotations"]
        shot_label_list = serialized["annotationResults"][0]["shotLabelAnnotations"]

        print("analyzed")

        ########################################################################################################################

        seg_data = pd.DataFrame()

        for i in range(len(seg_label_list)):
            if "categoryEntities" in seg_label_list[i]:
                seg_data = pd.concat([seg_data, pd.DataFrame([seg_label_list[i]["entity"]["description"],
                                                              seg_label_list[i]["categoryEntities"][0]["description"],
                                                              round(seg_label_list[i]["segments"][0]["confidence"],
                                                                    4)]).T])
            else:
                seg_data = pd.concat([seg_data, pd.DataFrame([seg_label_list[i]["entity"]["description"],
                                                              "NA",
                                                              round(seg_label_list[i]["segments"][0]["confidence"],
                                                                    4)]).T])

        seg_data.columns = ['Annotation', 'Annotation_Category', 'Confidence']
        seg_data = seg_data.sort_values('Confidence', ascending=False)
        seg_data = seg_data.reset_index(drop=True)
        seg_data["title"] = title
        seg_data["url"] = url
        seg_final = pd.concat([seg_final, seg_data], axis=0)

        ########################################################################################################################

        shot_data = pd.DataFrame()

        for i in range(len(shot_label_list)):
            if "categoryEntities" in shot_label_list[i]:
                for j in range(len(shot_label_list[i]["segments"])):
                    shot_start_time = shot_label_list[i]["segments"][j]["segment"]["startTimeOffset"]
                    shot_end_time = shot_label_list[i]["segments"][j]["segment"]["endTimeOffset"]
                    shot_len = str(pd.to_timedelta(shot_end_time) - pd.to_timedelta(shot_start_time))[7:15]

                    shot_data = pd.concat([shot_data, pd.DataFrame([shot_label_list[i]["entity"]["description"],
                                                                    shot_label_list[i]["categoryEntities"][0][
                                                                        "description"],
                                                                    round(
                                                                        shot_label_list[i]["segments"][0]["confidence"],
                                                                        4),
                                                                    str(pd.to_timedelta(shot_start_time))[7:15],
                                                                    str(pd.to_timedelta(shot_end_time))[7:15],
                                                                    shot_len]).T])
            else:
                for j in range(len(shot_label_list[i]["segments"])):
                    shot_start_time = shot_label_list[i]["segments"][j]["segment"]["startTimeOffset"]
                    shot_end_time = shot_label_list[i]["segments"][j]["segment"]["endTimeOffset"]
                    shot_len = str(pd.to_timedelta(shot_end_time) - pd.to_timedelta(shot_start_time))[7:15]

                    shot_data = pd.concat([shot_data, pd.DataFrame([shot_label_list[i]["entity"]["description"],
                                                                    "NA",
                                                                    round(
                                                                        shot_label_list[i]["segments"][0]["confidence"],
                                                                        4),
                                                                    str(pd.to_timedelta(shot_start_time))[7:15],
                                                                    str(pd.to_timedelta(shot_end_time))[7:15],
                                                                    shot_len]).T])

        shot_data.columns = ['Annotation', 'Annotation_Category', 'Confidence', 'Shot_Start_Time', 'Shot_End_Time',
                             'Shot_Length']
        shot_data = shot_data.sort_values(['Shot_End_Time', 'Confidence'], ascending=[True, False])
        shot_data = shot_data.reset_index(drop=True)
        shot_data["title"] = title
        shot_data["url"] = url
        shot_final = pd.concat([shot_final, shot_data], axis=0)

        with pd.ExcelWriter('C:\\S-Core\\output\\video\\{}.xlsx'.format(file_name)) as writer:
            seg_final.to_excel(writer, sheet_name='Segment', index=False,  encoding='utf-8')
            shot_final.to_excel(writer, sheet_name='Shot', index=False, encoding='utf-8')


if __name__ == '__main__':

    url_list = ["https://www.youtube.com/watch?v=IlQej3jQuZA",
                "https://www.youtube.com/watch?v=KB0oCXKvJYs"]

    title_list = ["iPhone 11 Pro Max Extreme stabilization test",
                  "TechTalk: Demonstrating Apple iPhone 11 Pro 4K Camera Video Zoom, HDR, Stabilization on the Beach"]

    VA = VideoAnalysis()
    for url, title in zip(url_list, title_list):
        file_dir, file_name = VA.download_video(url, title)
        VA.analyze_video(file_dir, file_name)
