from utils import get_categories
from utils import get_contents
from utils import API_URL

import os
import xbmc
import xbmcgui
import xbmcplugin

icons = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'icons')


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
            thumb = os.path.join(icons, '%s.png' % title.lower())
            xbmc.log(thumb, xbmc.LOGNOTICE)
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=title, thumbnailImage=thumb)
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
        content = get_contents(path)
        listing = []
        for cont in content:
            title = cont.get('name')
            url = "%s/%s" % (path, title)
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=title)
            if 'FILMS' in url:
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
        quality_folders = get_contents(path)
        listing = []
        for quality in quality_folders:
            title = quality.get('name')
            url = "%s/%s" % (path, title)
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=title)
            url = '{0}?action=qualitylisting&path={1}&quality={2}'.format(self.url, url, title)
            if 'FILMS' in url:
                url += '&type=FILMS'
            else:
                url += '&type=SERIES'
            is_folder = True
            listing.append((url, list_item, is_folder))

        # Add our listing to Kodi.
        xbmcplugin.addDirectoryItems(self.handle, listing, len(listing))
        # Add a sort method for the virtual folder items
        xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(self.handle)

    def list_season(self, path):
        """
        Create the list of playable videos in the Kodi interface.
        """
        season_folders = get_contents(path)
        listing = []
        for season in season_folders:
            title = season.get('name')
            url = "%s/%s" % (path, title)
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=title)
            url = '{0}?action=seasonlisting&path={1}&season={2}'.format(self.url, url, title)
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
        torrents = get_contents(path)
        listing = []
        for torrent in torrents:
            title = torrent.get('name')
            url = "%s/%s" % (path, title)
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=title)
            # Set additional info for the list item.
            list_item.setInfo('video', {'title': title, 'mediatype': 'video'})
            xbmc.log(path, xbmc.LOGNOTICE)
            # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
            # list_item.setArt({'thumb': videos['thumbnail'], 'icon': videos['thumbnail'], 'fanart': videos['thumbnail']})
            url = 'plugin://plugin.video.yatp/?action=play&torrent={0}&file_index=dialog'.format(url)
            is_folder = False
            listing.append((url, list_item, is_folder))

        # Set Content
        xbmcplugin.setContent(self.handle, 'episodes')
        # Add our listing to Kodi.
        xbmcplugin.addDirectoryItems(self.handle, listing, len(listing))
        # Add a sort method for the virtual folder items
        xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(self.handle)
