def buoyname(buoy:str):
    b = buoy.upper()
    lat = b[0]
    lon = b[2:-1]
    return(lat + '°' + b[1] + ' ' + lon + '°' + b[-1])

