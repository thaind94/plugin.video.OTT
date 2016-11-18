import sys
import urllib
import urlparse
from urlparse import parse_qsl
import xbmc
import xbmcgui
import xbmcplugin
import json
import os.path
import catg
import cList
from bs4 import BeautifulSoup
import time
import thread


def getListChannel():
  arr = []
  url = 'http://vtvgo.vn/xem-truc-tuyen.html'
  htmltext = urllib.urlopen(url).read()
  soup = BeautifulSoup(htmltext)
  list_items = soup.find_all("div", class_="item")
  i = 0
  for item in list_items:
    link = {}
    images = item.find_all("img")
    link_image = images[0].get("src")
    path_parts = link_image.rpartition('/')
    path_parts = path_parts[2].rpartition('.')
    i += 1
    link["id"] = path_parts[0]
    link["image"] = link_image
    link["channel"] = "VTV" + str(i)
    arr.append(link)
    pass

  return arr
  pass
def get_chanel(id_):
  params = {'epg_id': str(id_),'type': '1'}
  url = 'http://vtvgo.vn//get-program-channel?'
  url = url + urllib.urlencode(params)
  htmltext = urllib.urlopen(url).read()
  j = json.loads(htmltext)
  return j["data"]
  pass

def getvideo(id_):
  params = {'epg_id': str(id_),'id': '-1', 'type': '2'}
  url = 'http://vtvgo.vn//get-program-channel?'
  url = url + urllib.urlencode(params)
  htmltext = urllib.urlopen(url).read()
  j = json.loads(htmltext)
  return j
  pass

def list_categories():
  listing = []
  categories = catg.categories.keys()
  for category in categories:
    list_item = xbmcgui.ListItem(label = category, thumbnailImage = catg.categories[category][0]['thumb'])
    list_item.setProperty('fanart_image', catg.categories[category][0]['fanart'])
    list_item.setInfo('video', {'title': category, 'genre': category})
    url = '{0}?action=listing&category={1}'.format(base_url, category)
    is_folder = True
    listing.append((url, list_item, is_folder))
  xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
  xbmcplugin.endOfDirectory(addon_handle)

def list_play(category):
  listing = []
  if category == 'LiveTV':
    for channel in List:
      list_item = xbmcgui.ListItem(label = channel, thumbnailImage = cList.channels[channel][0]['thumb'])
      list_item.setProperty('fanart_image', cList.channels[channel][0]['fanart'])
      # list_item.setProperty('IsPlayable', 'true')
      url = '{0}?action=play&channel={1}&id={2}'.format(base_url, channel, get_id(channel))
      is_folder = False
      listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(addon_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(addon_handle)
  # elif category == 'Videos':
def get_id(name):
  for channel in channels:
    if channel['channel'] == name:
      return channel['id']
      break
  pass
def play_channel(id_):
  path = get_chanel(id_)
  # play_item = xbmcgui.ListItem(path = path)
  # xbmcplugin.setResolvedUrl(addon_handle, True, listitem = play_item)
  return path
def timer(newthread,delay):
    time.sleep(delay)
    xbmc.Player().playnext()

def router(paramstring):
  params = dict(parse_qsl(paramstring[1:]))
  if params:
    if params['action'] == 'listing':
      list_play(params['category'])
    elif params['action'] == 'play': # and params['category' == 'LiveTV'] // and params['category' == 'Videos']
      # playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
      # url = 'http://123.30.238.109/live/_definst_/vtv1-mid.m3u8?t=43571b5eaa2157c04cda30840d61f59d&e=1479464440'
      # playlist.add(url = url, index = 2)
      # url = 'http://123.30.238.109/live/_definst_/vtv1-high.m3u8?t=43571b5eaa2157c04cda30840d61f59d&e=1479464440'
      # playlist.add(url = url, index = 1)
      playlist = play_channel(params['id'])
      xbmc.Player().play(playlist)
      # thread.start_new_thread(timer,('newthread', 10,))

      # play_channel(params['id'])
  else:
    list_categories()
  pass
if __name__ == '__main__':
  base_url = sys.argv[0]
  addon_handle = int(sys.argv[1])
  List = cList.channels.keys()
  channels = getListChannel()
  router(sys.argv[2])