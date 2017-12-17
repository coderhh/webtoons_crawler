# python3
# combine pictures from same episode together
from PIL import Image
import numpy as np
import os, logging, time
logging.basicConfig(filename='crawler.log', filemode='w', level=logging.DEBUG,format=' %(asctime)s - %(levelname)s- %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
start_time = time.time()

def combineV(folderPath):
    # get all picture name 
    imagesNameList = sorted(os.listdir(folderPath))
    # create picture path
    imagesList = [os.path.join(folderPath,i) for i in imagesNameList]
    
    imgs = [ Image.open(i) for i in imagesList ]
    
    max_img_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[len(imgs)-1][1]
    
    img_merge = np.vstack( (np.asarray( i.resize(max_img_shape,Image.ANTIALIAS) ) for i in imgs ) )
    img_merge = Image.fromarray( img_merge)
    combineImagePath = os.path.join('combine_v',folderPath+'_v.jpg')
    #os.remove(combineImagePath)
    img_merge.save(combineImagePath)


def combineH(folderPath):
    # get all picture name 
    imagesNameList = sorted(os.listdir(folderPath))
    # create picture path
    imagesList = [os.path.join(folderPath,i) for i in imagesNameList]
    
    imgs = [ Image.open(i) for i in imagesList ]
    
    max_img_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[len(imgs)-1][1]
    
    img_merge = np.hstack( (np.asarray( i.resize(max_img_shape,Image.ANTIALIAS) ) for i in imgs ) )
    img_merge = Image.fromarray( img_merge)
    combineImagePath = os.path.join('combine_h',folderPath+'_v.jpg')
    #os.remove(combineImagePath)
    img_merge.save(combineImagePath)

def combine(folderPath):
    imagesNameList = sorted(os.listdir(folderPath))
    imagesList = [os.path.join(folderPath,i) for i in imagesNameList]
    imgs = [ Image.open(i) for i in imagesList ]
    imgestest = imgs[:50]
    min_img_shape = sorted( [(np.sum(i.size), i.size ) for i in imgestest])[0][1]
    reduced_min_img_shape =  [x/100 for x in min_img_shape]
    img_merge = np.hstack( (np.asarray( i.resize(min_img_shape,Image.ANTIALIAS) ) for i in imgestest ) )
    
    img_merge = Image.fromarray(img_merge)
    
    img_merge.save('combine100.jpg')

    
    
combine('combine_v')

#episodeList = [x[0] for x in os.walk('.')]
#for episodeFolder in episodeList:
 #   if 'episode' in episodeFolder:
  #      episodestart_time = time.time()
   #     logging.info('Combining %s...' % episodeFolder)
    #    combineH(episodeFolder)
     #   logging.info("episodeComing time--- %s seconds ---" % (time.time() - episodestart_time))
      #  logging.info("Total time--- %s seconds ---" % (time.time() - start_time))

    