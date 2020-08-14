#import pexif
import piexif
import piexif.helper
from PIL import Image 

def dump_exif():
    #file_name = "/Users/junlin/test/gps/IMG_3777.JPG"
    file_name = "/Users/junlin/test/gps/no_gps.jpg"
    exif_dict = piexif.load(file_name)
    for ifd in ("0th", "Exif", "GPS", "1st"):
        print("===================", ifd, "=====================")
        for tag in exif_dict[ifd]:
            print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])

if __name__ == '__main__':
    dump_exif()
    file_name = "/Users/junlin/test/gps/IMG_7470.JPG"

    #jf = pexif.JpegFile.fromFile(")
    #(lat, lng) = (121.624388, 31.213554)
    #jf.set_geo(lat, lng)
    #new_file = jf.writeString()
    #print(new_file)

    # im = Image.open(file_name)
    # exif_dict = piexif.load(im.info["exif"])
    # w, h = im.size
    # exif_dict["GPS"]["GPSLongitude"] = 121.624388
    # exif_dict["GPS"]["GPSLatitude"] = 31.213554
    # exif_bytes = piexif.dump(exif_dict)
    # im.save("/Users/junlin/test/gps/IMG_7470_gps.JPG", "jpeg", exif=exif_bytes, quality=100)

    # exif_dict = piexif.load(file_name)
    # user_comment = piexif.helper.UserComment.dump(u"{\"comment\":\"this is test!\"}")
    # exif_dict["Exif"][piexif.ExifIFD.UserComment] = user_comment
    # exif_raw = piexif.dump(exif_dict)
    # piexif.insert(exif_raw, "/Users/junlin/test/gps/no_gps.JPG")

    # gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),  # BYTE, count 4
    #        piexif.GPSIFD.GPSAltitudeRef: 1,  # BYTE, count 1 ... also be accepted '(1,)'
    #        }
    gps_ifd = {piexif.GPSIFD.GPSVersionID: (2, 0, 0, 0),  # BYTE, count 4
                piexif.GPSIFD.GPSLongitudeRef: u"E",
                piexif.GPSIFD.GPSLongitude: ((121, 1), (28, 1), (1816, 100)),
                piexif.GPSIFD.GPSLatitudeRef: u"N",
                piexif.GPSIFD.GPSLatitude: ((31, 1), (12, 1), (4965, 100)),
           }
# GPSLatitudeRef b'N'
# GPSLatitude ((31, 1), (12, 1), (4965, 100))
# GPSLongitudeRef b'E'
# GPSLongitude ((121, 1), (28, 1), (1816, 100))
# GPSAltitudeRef 0
# GPSAltitude (80089, 2553)
# GPSSpeedRef b'K'           
    exif_dict = {"GPS":gps_ifd}
    exif_raw = piexif.dump(exif_dict)
    piexif.insert(exif_raw, "/Users/junlin/test/gps/no_gps.JPG")