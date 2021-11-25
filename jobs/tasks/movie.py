from application import app, db
import requests
import os
import time
import hashlib
import json
import re
from bs4 import BeautifulSoup
from common.lib.DataHelper import getCurrentTime
from urllib.parse import urlparse
from common.models.movie import Movie
from datetime import datetime
'''
python manager.py runjob -m movie -a list | parse
'''


class JobTask():
    def __init__(self):
        self.source = "boxofficemojo"
        self.url = "https://www.boxofficemojo.com/year/2021"
        self.path = "/tmp/%s/" % (self.source)

    '''
    First: get the list (html)，parse html to get info such as name, href for further info
    Second: parse the html for further info
    '''

    def run(self, params):
        act = params['act']
        self.date = getCurrentTime(frm="%Y%m%d")
        if act == "list":
            self.getList()
            self.parseInfo()
        elif act == "parse":
            self.parseInfo()

    def getList(self):
        path_root = self.path + self.date
        path_list = path_root + "/list"
        path_info = path_root + "/info"
        path_json = path_root + "/json"

        self.makeSuredirs(path_root)
        self.makeSuredirs(path_list)
        self.makeSuredirs(path_info)
        self.makeSuredirs(path_json)

        # save the basic html
        tmp_path = path_list + "/1"
        tmp_url = self.url
        app.logger.info("get list : " + tmp_url)
        if not os.path.exists(tmp_path):
            tmp_content = self.getHttpContent(self.url)
            self.saveContent(tmp_path, tmp_content)
            time.sleep(0.3)

        # parse the html
        tmp_content = self.getContent(tmp_path)
        items_data = self.parseList(tmp_content)
        if items_data:
            for item in items_data:
                tmp_json_path = path_json + "/" + item['hash']
                tmp_info_path = path_info + "/" + item['hash']
                # tmp_vid_path = path_vid + "/" + item['hash']
                if not os.path.exists(tmp_json_path):
                    self.saveContent(tmp_json_path, json.dumps(
                        item, ensure_ascii=False))

                if not os.path.exists(tmp_info_path):
                    tmp_content = self.getHttpContent(item['url'])
                    self.saveContent(tmp_info_path, tmp_content)

                time.sleep(0.3)

    def parseList(self, content):
        data = []
        tmp_soup = BeautifulSoup(str(content), "html.parser")
        tmp_list = tmp_soup.select("td.mojo-field-type-release")

        for tmp_item in tmp_list:
            tmp_target = tmp_item.select("a")
            tmp_name = tmp_target[0].text
            tmp_href = tmp_target[0]['href']
            if "http:" not in tmp_href:
                tmp_href = "https://www.boxofficemojo.com" + tmp_href
            tmp_data = {
                "name": tmp_name,
                "url": tmp_href,
                "hash":  hashlib.md5(tmp_href.encode("utf-8")).hexdigest()
            }
            data.append(tmp_data)

        return data

    def parseInfo(self):
        path_root = self.path + self.date
        path_info = path_root + "/info"
        path_json = path_root + "/json"

        for filename in os.listdir(path_info):
            tmp_json_path = path_json + "/" + filename
            tmp_info_path = path_info + "/" + filename

            tmp_data = json.loads(self.getContent(
                tmp_json_path), encoding="utf-8")
            tmp_content = self.getContent(tmp_info_path)
            tmp_soup = BeautifulSoup(tmp_content, "html.parser")

            try:
                tmp = tmp_soup.select("div.mojo-summary-values div")
                for item in tmp:
                    if item.select("span")[0].getText() == "Release Date":
                        tmp_pub_date = item.select("span")[1].getText()
                    elif item.select("span")[0].getText() == "Genres":
                        tmp_genre = item.select("span")[1].getText()
                    elif item.select("span")[0].getText() == "Running Time":
                        tmp_length = item.select("span")[1].getText()
                tmp_desc = ""
                if len(tmp_soup.select("p.a-size-medium")) != 0:
                    tmp_desc = tmp_soup.select("p.a-size-medium")[0].getText()
                tmp_pic_list = tmp_soup.select("div.mojo-posters img")
                tmp_pics = []
                for tmp_pic in tmp_pic_list:
                    tmp_pics.append(tmp_pic['src'])

                tmp_gross = tmp_soup.select("span.money")[
                    0].getText().replace('$', '').replace(',', '')

                try:
                    tmp_data['release_date'] = datetime.strptime(
                        tmp_pub_date, '%b %d, %Y')
                except:
                    pass

                tmp_data['gross'] = tmp_gross
                tmp_data['description'] = tmp_desc
                tmp_data['genre'] = tmp_genre
                tmp_data['length'] = tmp_length
                tmp_data['source'] = self.source
                tmp_data['create_time'] = tmp_data['update_time'] = getCurrentTime()
                if tmp_pics:
                    tmp_data['cover_pic'] = tmp_pics[0]
                    tmp_data['pics'] = json.dumps(tmp_pics)

                tmp_movie_info = Movie.query.filter_by(
                    hash=tmp_data['hash']).first()

                if tmp_movie_info:
                    continue

                tmp_model_movie = Movie(**tmp_data)
                db.session.add(tmp_model_movie)
                db.session.commit()

            except Exception as e:
                print(e)
                break
                continue
        return True

    def getHttpContent(self, url):
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None

            return r.content

        except Exception:
            return None

    def saveContent(self, path, content):
        if content:
            with open(path, mode="w+", encoding="utf-8") as f:
                if type(content) != str:
                    content = content.decode("utf-8")

                f.write(content)
                f.flush()
                f.close()

    def getContent(self, path):
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()

        return ''

    def makeSuredirs(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
