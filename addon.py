from urlparse import parse_qsl
from torrent import TorrentHandler

import sys
import xbmcaddon


addon = xbmcaddon.Addon()

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

vh = TorrentHandler(_handle, _url)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    :param paramstring:
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if 'content_type' in params:
            if params['content_type'] == 'video':
                vh.list_categories()
        else:
            if 'action' in params:
                if params['action'] == 'categorylisting':
                    # Display the list of videos in a provided category.
                    vh.list_content(params['path'])
                elif params['action'] == 'contentlisting':
                    # Display the list of videos in a provided category.
                    vh.list_quality(params['path'])
                elif params['action'] == 'qualitylisting':
                    # Display the list of videos in a provided category.
                    vh.list_torrent(params['path'])
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        vh.list_categories()

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
