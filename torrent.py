from utils import get_categories
from utils import get_contents
from utils import get_qualities
from utils import get_torrents
from utils import API_URL

import xbmc
import urllib2
import urlparse
import xbmcgui
import xbmcplugin


class TorrentHandler(object):
    def __init__(self, handle, url):
        self.handle = handle
        self.url = url

    def list_categories(self):
        """
        Create the list of video programs in the Kodi interface.
        """
        categories = get_categories()
        listing = []
        for cat in categories:
            title = cat.get('name')
            path = "%s/%s" % (API_URL, title)
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=title)
            url = '{0}?action=categorylisting&path={1}&category={2}'.format(self.url, path, title)
            is_folder = True
            listing.append((url, list_item, is_folder))

        # Add our listing to Kodi.
        xbmcplugin.addDirectoryItems(self.handle, listing, len(listing))
        # Add a sort method for the virtual folder items
        xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(self.handle)

    def list_content(self, path):
        """
        Create the list of episodes for a given program
        """

        xbmc.log(path, xbmc.LOGNOTICE)
        content = get_contents(path)
        listing = []
        for cont in content:
            title = cont.get('name')
            url = "%s/%s" % (path, title)
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=title)
            if 'FILMS' in path:
                mediatype = 'movie'
                # Set Content
                xbmcplugin.setContent(self.handle, 'movies')
            else:
                mediatype = 'tvshow'
                # Set Content
                xbmcplugin.setContent(self.handle, 'tvshows')
            list_item.setInfo('video', {'title': title, 'mediatype': mediatype})
            url = '{0}?action=contentlisting&path={1}&content={1}'.format(self.url, url, title)
            is_folder = True
            listing.append((url, list_item, is_folder))

        # Add our listing to Kodi.
        xbmcplugin.addDirectoryItems(self.handle, listing, len(listing))
        # Add a sort method for the virtual folder items
        xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(self.handle)

    def list_quality(self, path):
        """
        Create the list of playable videos in the Kodi interface.
        """
        quality_folders = get_qualities(path)
        listing = []
        for quality in quality_folders:
            title = quality.get('name')
            url = "%s/%s" % (path, title)
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=title)
            url = '{0}?action=qualitylisting&path={1}&quality={2}'.format(self.url, url, title)
            is_folder = True
            listing.append((url, list_item, is_folder))

        # Add our listing to Kodi.
        xbmcplugin.addDirectoryItems(self.handle, listing, len(listing))
        # Add a sort method for the virtual folder items
        xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(self.handle)

    def list_torrent(self, path):
        """
        Create the list of playable videos in the Kodi interface.
        """
        torrents = get_torrents(path)
        listing = []
        for torrent in torrents:
            title = torrent.get('name')
            url = "%s/%s" % (path, title)
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=title)
            # Set additional info for the list item.
            list_item.setInfo('video', {'title': title, 'mediatype': 'video'})
            # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
            # list_item.setArt({'thumb': videos['thumbnail'], 'icon': videos['thumbnail'], 'fanart': videos['thumbnail']})
            list_item.setProperty('IsPlayable', 'true')
            torrent_url = ''
            url = 'plugin://plugin.video.yatp/?action=play&torrent={0}'.format(torrent_url)
            is_folder = False
            listing.append((url, list_item, is_folder))

        # Set Content
        xbmcplugin.setContent(self.handle, 'episodes')
        # Add our listing to Kodi.
        xbmcplugin.addDirectoryItems(self.handle, listing, len(listing))
        # Add a sort method for the virtual folder items
        xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(self.handle)
