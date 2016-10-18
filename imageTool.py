import os
import sys
from PIL import Image
extensions = ['.jpg', '.png']
operations = ['resize', 'rotate', 'change format', 'change color mode']

def printOptions():
    print('Options:')
    print('1. One Picture')
    print('2. All Pictures')
    print('3. Range of Pictures') 

    return int(input('>>'))

def makeDir(di):
    newdi = os.path.join(os.getcwd(), di)
    if len(newdi) > len(os.getcwd()):
        if not os.path.isdir(newdi):
            os.mkdir(newdi)
            
    return newdi

def main():
    while True:
        images = []
        for file in os.listdir('.'):
            fileName, fileExt = os.path.splitext(file)
            if fileExt in extensions:
                images.append(file)

        if len(images) == 0:
            print('No compatable images in directory')
            return
        
        print('\n\nImages in directory:')
        for number, image in enumerate(images):
            print('%d. %s' % (number, image))

        print('\n\nWhat operation would you like to do:')
        for num, op in enumerate(operations):
            print('%d. %s' % (num, op))

        try:
            uinput = input('>>') 

            if str(uinput) == 'wq':
                return
            else:
                uinput = int(uinput)
                
            if uinput < 0 or uinput > len(operations):
                raise
            
        except:
            print('Not a valid input')
            continue
      
        op = operations[uinput]

        try:
            if op == "resize":
                size = str(input('Enter both dimensions seperated by a comma:')).split(',')
                size = [int(x) for x in size]
                
                o = printOptions()

                di = str(input('Local directory to save to(leave blank for overwrite):'))
                di = makeDir(di)
                
                if o == 1:
                    num = int(input('Picture index:'))

                    img = Image.open(images[num])
                    img = img.resize(size)
                    if di == None:
                        img.save(images[num])
                    else: 
                        img.save('%s/%s' % (di, images[num]))

                elif o == 2:
                    for img in images:
                        im = Image.open(img)
                        im = im.resize(size)
                        if di == None:
                            im.save(img)
                        else:
                            im.save('%s/%s' % (di, img))
                else:
                    ran = str(input('Enter range seperated by comma:')).split(',')
                    for img in images[int(ran[0]):int(ran[1]) + 1]:
                        im = Image.open(img)
                        im = im.resize(size)
                        if di == None:
                            im.save(img)
                        else:
                            im.save('%s/%s' % (di, img))

            elif op == "rotate":
                dg = int(input('Degrees:'))

                o = printOptions()

                di = str(input('Local directory to save to(leave blank for overwrite):'))
                di = makeDir(di)

                if o == 1:
                    num = int(input('Picture index:'))

                    img = Image.open(images[num])
                    img = img.rotate(dg)
                    if di == None:
                        img.save(images[num])
                    else:
                        img.save('%s/%s' % (di, images[num]))

                elif o == 2:
                    for img in images:
                        im = Image.open(img)
                        im = im.rotate(dg)
                        if di == None:
                            im.save(img)
                        else:
                            im.save('%s/%s' % (di, img))
                else:
                    ran = str(input('Enter range seperated by comma:')).split(',')
                    for img in images[int(ran[0]):int(ran[1]) + 1]:
                        im = Image.open(img)
                        im = im.rotate(dg)
                        if di == None:
                            im.save(img)
                        else:
                            im.save('%s/%s' % (di, img))
                
            elif op == "change format":
                newf = str(input('New format:'))

                o = printOptions()

                di = str(input('Local directory to save to(leave blank for overwrite):'))
                di = makeDir(di)

                if o == 1:
                    num = int(input('Picture index:'))


                    img = Image.open(images[num])
                    name, ext = os.path.splitext(images[num])
                    if di == None:
                        img.save('%s.%s' % (name, newf))
                    else:
                        img.save('%s/%s.%s' % (di, name, newf))

                elif o == 2:
                    for img in images:
                        im = Image.open(img)
                        name, ext = os.path.splitext(img)
                        if di == None:
                            newname = '%s.%s' % (name, newf)
                            im.save(newname)
                        else:
                            newname = '%s/%s.%s' % (di, name, newf)
                            im.save(newname)
                else:
                    ran = str(input('Enter range seperated by comma:')).split(',')
                    for img in images[int(ran[0]):int(ran[1]) + 1]:
                        im = Image.open(img)
                        name, ext = os.path.splitext(img)
                        if di == None:
                            im.save('%s.%s' % (name, newf))
                        else:
                            im.save('%s/%s.%s' % (di, name, newf))
                
            elif op == "change color mode":
                newc = str(input('New color mode:'))

                o = printOptions()
                
                di = str(input('Local directory to save to(leave blank for overwrite):'))
                di = makeDir(di)

                if o == 1:
                    num = int(input('Picture index:'))

                    img = Image.open(images[num])
                    img = img.convert(mode= newc)
                    if di == None:
                        img.save(images[num])
                    else:
                        img.save('%s/%s' % (di, images[num]))

                elif o == 2:
                    for img in images:
                        im = Image.open(img)
                        im = im.convert(mode= newc)
                        if di == None:
                            im.save(img)
                        else:
                            im.save('%s/%s' % (di, img))
                else:
                    ran = str(input('Enter range seperated by comma:')).split(',')
                    for img in images[int(ran[0]):int(ran[1]) + 1]:
                        im = Image.open(img)
                        im = im.convert(mode= newc)
                        if di == None:
                            im.save(img)
                        else:
                            im.save('%s/%s' % (di, img))

        except:
            print(str(sys.exc_info()[0]))
            print('\nInvalid Input\n\n')
            continue

                        
if __name__ == '__main__':
    main()
