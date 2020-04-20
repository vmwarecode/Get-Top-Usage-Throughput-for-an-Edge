#
# Sample Script used to calculate Edge Top average throughput in the last 5 days..
#
# Usage: VC_USERNAME='super@velocloud.net' VC_PASSWORD='vcadm!n' python XXXX.py
#

import os
from client import *
import calendar
from datetime import datetime, timedelta

# EDIT THESE
VCO_HOSTNAME = 'vco33.velocloud.net'
ENTERPRISE_ID = 1 # As may be found e.g. in web UI URL path under Customer
edgeId = 6

def main():

    client = VcoRequestManager(VCO_HOSTNAME)
    client.authenticate(os.environ['VC_USERNAME'], os.environ['VC_PASSWORD'], is_operator=os.environ.get('VC_OPERATOR', True))

    # Input Provisioning File name


    print('### GETTING EDGE Link series ###')

    Sample_Interval = 0


    try:

        date = datetime.utcnow()
        date_before = date - timedelta(days=5)
        start = int(calendar.timegm(date_before.timetuple())) * 1000

        params = {"edgeId": edgeId, "enterpriseId": ENTERPRISE_ID, "interval": {"start": start},"with": ["bytesRx","bytesTx"]}

        res = client.call_api('/metrics/getEdgeLinkSeries', params )

    except Exception as e:
            print('Failed to get link series of Edge "%d"' % edgeId)
            print(e)

    Sample_Interval = res[0]['series'][0]['tickInterval'] / 1000

    Total_BW_List = []




    for link in res :


        bytesRX = link['series'][0]['data']   

        bytesRX_list = [0 if v is None else v for v in bytesRX]

        bytesTX = link['series'][1]['data']

        bytesTX_list = [0 if v is None else v for v in bytesTX]

        Link_BW = [x + y for x, y in zip(bytesTX_list, bytesRX_list) ]

        if len(Total_BW_List) == 0 :

            Total_BW_List = Link_BW

        else :

            Total_BW_List = [x + y for x, y in zip(Total_BW_List, Link_BW)]


    Total_BW_List.sort()

    Second_to_highest_bw_Bytes = Total_BW_List[-1]

    BW_in_Mbps = (Second_to_highest_bw_Bytes*8)/(float(Sample_Interval*1000*1000))

    BW_in_Mbps = round(BW_in_Mbps , 3)

    print ('Top usage throughput for the last 5 days is '+ str(BW_in_Mbps)+" Mbps")


if __name__ == '__main__':
    main()        



