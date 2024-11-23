import google.generativeai as genai
import os
import json
'''
categories = {'sheet music':"the name might the name of a song and will be of the .pdf format",
                "wallpaper":"it will usually be the name of the artist and then it might describe a scenery and will be of image format",
                "academic":"it might be of pdf, ppt or something like that",
                "apps":"it might be a setup and might be of the format .exe .amd64 .mis etc..",
                "miscellaneous": "anything that doesn't fall under these categories"
                }

files = ['One summers day joe hishaishi.pdf','alena-aename-mountains.jpg','FALLSEM2024-25_BSTS201P_SS_CH2024250103835_Reference_Material_I_09-08-2024_Rebus_Puzzles_2022_(4).pptx','mysql-installer-web-community-8.0.39.0.msi']
'''

def classify(categories:dict,files:list):

    genai.configure(api_key='AIzaSyDXTxCjooLl2OLBIwGW_mO2pcKsORUXCWc')

    model = genai.GenerativeModel("gemini-1.5-flash")

    format_spec_1 = "i'll give you a list of file names and you have to classify the file as following, return the answer in this format {name of the file exactly as given in the input:name of the category exactly as given}"
    format_spec_2 = "here are the file names-"

    


    categories_str = ''
    c = 1

    for i in categories:
        categories_str += str(c)+'.'+i + ' : ' + categories[i]+', '
        c+=1

    categories_str = categories_str[:-2]
    files_str = str(files)[1:-1]




    #response = model.generate_content("i'll give you a list of file names and you have to classify the file as following, return the answer in this format {index of file:index of type} where index of file is a number which refers to the index of the file for example if its the first file then index should be 1 and index of type is a number which refers to the index of the type of the file for ex if its sheet music its supposed to be 1 - 1.sheet music-the name might the name of a song and will be of the .pdf format 2.wallpaper- it will usually be the name of the artist and then it might describe a scenery and will be of image format 3.Academic : it might be of pdf, ppt or something like that 4.App : it might be a setup and might be of the format .exe .amd64 .mis etc.. 5. miscellaneous: anything that doesn't fall under these categories. here are the file names 'One summers day joe hishaishi.pdf','alena-aename-mountains.jpg','FALLSEM2024-25_BSTS201P_SS_CH2024250103835_Reference_Material_I_09-08-2024_Rebus_Puzzles_2022_(4).pptx','mysql-installer-web-community-8.0.39.0.msi'")
    response = model.generate_content(' '.join([format_spec_1,categories_str,format_spec_2,files_str]))

    response_clean = ''
    flag = False
    
    for i in response.text:

        if i == '}':
            flag = False
        if flag:
            response_clean+=i
        if i == '{':
            flag = True

    return json.loads('{'+response_clean+'}')

    files_classified = {}
    for i in response_clean.split(','):
        i = i.strip()
        i = i.split(':')
        files_classified[i[0]] = i[1]

    return files_classified

def get_file_list(path):
    lis = []
    for i in os.listdir(path):

        if not os.path.isdir(path+'\\'+i):
            lis.append(i)
    return lis



def create_files(folders,path):
    for i in folders:
        if not os.path.exists(path+'\\'+str(i)):
            os.mkdir(path+'\\'+str(i))



def main():
    os.system('cls')

    path = input('enter path: ')
    n = int(input('enter the number of different types: '))
    categories = {}
    for i in range(n):
        n1 = input('enter the name of category(its what the folder is going to be named): ')
        n2 = input('explain the characteristics as detailed as possible (more detailed means higher accuracy): ')
        print()
        categories[n1] = n2

    os.system('cls')
    print('path:',path)
    for i in categories:
        print(i)
        print(categories[i])
        print()
    if input('are you sure you want to continue? y/n ').lower() == 'y':
        os.system('cls')
        create_files(categories.keys(),path)

        while True:
            try: 
                files = get_file_list(path)
                if len(files)>10:
                    files_temp = files[:10]
                elif files:
                    files_temp = files
                else:
                    break
                
                print(len(files),'left')

                classified_dict = classify(categories,files_temp)
                
                for i in classified_dict:
                    
                    
                        os.rename(path+'\\'+i, path+'\\'+classified_dict[i]+'\\'+i)
            except:
                pass
    
    print('completed')



if __name__ == '__main__':
    main()