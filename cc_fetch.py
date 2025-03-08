import cmd
import os
import tqdm
import requests




class CC_Fetch(cmd.Cmd):
    
    prompt = 'ccf:\\>'

    ruler = '-'

    base_addr = 'https://index.commoncrawl.org/'

    domain_list = []

    #list of the most recent crawls
    #last updated 21 FEB 2025
    crawls = [
        'CC-MAIN-2025-05-index',
        'CC-MAIN-2024-51-index',
        'CC-MAIN-2024-46-index',
        'CC-MAIN-2024-42-index',
        'CC-MAIN-2024-38-index',
        'CC-MAIN-2024-33-index',
        'CC-MAIN-2024-30-index',
        'CC-MAIN-2024-26-index',
        'CC-MAIN-2024-22-index',
        'CC-MAIN-2024-18-index',
        'CC-MAIN-2024-10-index',
    ]

    crawl = crawls[0]

    chunk_size = 1024

    use_curl = True

    intro_1='Welcome to cc_fetch!\n\n'
    intro_2='By default cc_fetch will create text files with links to web archives of the domains you specify.\n'
    intro_3='If curl is installed on your sytem, you can use it to download the archives.\n\n'
    intro_4='See Terms of Use for Common Crawl data here: https://commoncrawl.org/terms-of-use\n\n'
    intro_5='Use [TAB] for command completion.\nType "help" or "?" for a list of commands.\n'
    intro_6=f'Using crawl: {crawl}\nChunk size: {chunk_size}\n'
    intro = intro_1+intro_2+intro_3+intro_4+intro_5+intro_6

    def get_urls(self, domain):

        indexes = requests.get(self.base_addr+self.crawl+'?url='+domain)

        #ensure there is an index for the domain before proceeding
        if indexes.status_code != 200:
            print(f'ERROR: received status code {indexes.status_code}')
            pass

        indexes_split = indexes.text.split('\n')

        file_names = []

        for name in indexes_split:
            
            start = name.find('"crawl')+1
            end = name.find('.gz')+3
            
            file_names.append(name[start:end])
            

        #create a list of urls for the indexes and download request
        urls = []

        for name in file_names:

            prefix = 'https://data.commoncrawl.org/'
            urls.append(prefix+name)

        return urls
    
    def do_no_curl(self, inp):
        '''
        Don't save list of files for use with curl. This option will force cc_fetch to attempt the download.
        '''
        if self.use_curl == True:
            no_curl_conf = input('WARNING: Using curl is the reccomended download strategy.\nAre you sure you want to continue [y/n]?\n').lower()
            if 'y' in no_curl_conf:
                self.use_curl = False
                print('Confirmed. No url file will be saved. The archive will be downloaded directly.')
            else:
                print('Cancelling...')

        elif self.use_curl == False:
            no_curl_conf = input('Using curl is the reccomended download strategy.\nUse curl [y/n]?\n').lower()
            if 'y' in no_curl_conf:
                self.use_curl = True
                print('Confirmed. The url file will be saved.')
            else:
                print('Cancelling...')
            

    def do_crawl( self, inp):
        '''
        Choose which crawl to use.
        '''
        print(f'Currently using crawl: {self.crawl}')

        change_crawl = input('Would you like to choose a different crawl [y/N]?\n').lower()

        if 'y' in change_crawl:
            print('Available Crawls:')
            for i,crawl in enumerate(self.crawls):
                print(f'{i}) {crawl}')

            print(f'{i+1}) Other')
            
            
            try:
                selection = int(input('Select new crawl:'))
                if selection == i+1:
                    print('Additional crawls can be found at:\nhttps://commoncrawl.org/overview\n')
                    self.crawl = input('Enter new crawl:\n')
                    print(f'Crawl set to {self.crawl}')

                else:
                    self.crawl = self.crawls[selection]
                    print(f'Crawl set to {self.crawl}')

            except Exception as e:
                print(f'ERROR: {e}')
                print(f'Try entering a number between 0 and {i+1}.')

        else:
            print('Cancelling')

    def do_chunk(self, inp):
        '''
        Short: ch
        If downloading with cc_fetch, the downloads are broken into chunks. This option allows you to change the chunk size.
        '''
        
        try:
            chunk = int(input(f'The current download chunk size is set to {self.chunk_size}.\nSet it to:'))

        except Exception as e:
            print(f'ERROR: {e}')
            print('Try entering an interger.')

    def do_domains(self,inp):
        '''
        Short: d
        Create a list of domains to seach the for in the crawl. This will overwite the existing list.
        '''

        cont = True
        self.domain_list = []
        print('Create a list of domains to search for.\nEnter an empty line or type ''exit'' to return to the main program.')
        while cont == True:
            user_response = input('add domain:')
            if user_response == '' or user_response == 'exit':
                cont = False
                print('Domain list complete.')

            else:
                self.domain_list.append(user_response)

    def do_list_domains(self,inp):
        '''
        Short: lsd
        Show the list of domains.
        '''
        for domain in self.domain_list:
            print(domain)
  
    def do_quit(self, inp):
        '''
        Short: q
        Exits the program.
        '''
        print('Exiting...')
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def do_download(self,inp):
        '''
        Short: dl
        This command searches the selected crawl for archives of the domains in the domain list. When using the default 
        settings, no files will be downloaded. Instead, files containing urls of the archives will be written. The 
        archives can then easily be downloaded with curl. Regardless of using curl, cc_fetch attempts to provide an 
        estimate of the size of the download(s).
        '''
        
        grand_total = 0

        if self.use_curl == True:
            print(f'\nTo download with curl use the command "curl -LOC - -K [domain-urls.txt]"')
            print('For more options use "man curl" or "curl -h"\n\n')

        for domain in self.domain_list:
            
            urls = self.get_urls(domain)

            if self.use_curl == True:
                #save the url file
                urls_filename = domain.replace('.','_')+'-urls.txt'
                with open(urls_filename,'w') as file:
                    for url in urls[:-1]:
                        line = 'url='+url+'\n'
                        file.write(line)

                print(f'Url file written as {urls_filename}')
                

            #get sizes of warc files
            total_size = 0

            #find size of downloaded archives
            for i,url in enumerate(urls):
                
                if url != '':
                    response = requests.get(url, stream=True)
                    #print('='*20,i,'='*20)
                    
                    #check if theres content in the url, add its size to total
                    try:
                        
                        dl_size = int(response.headers['content-length'])
                        total_size += dl_size

                    except:
                        pass
                    
                        
            grand_total += total_size
            print(f'Downloading the archive {domain} will require {round(total_size/1000000000,2)}Gb\n')

        print(f'Total download size {round(grand_total/1000000000,2)}Gb\n')

        if self.use_curl == False:
            proceed = input('Would you like to proceed with download [y/n]?\n').lower()

            if 'n' in proceed:
                print('Cancelling...')
                

            elif 'y' in proceed:
                print('Downloading\n')
               
                #get urls
                for domain in self.domain_list:
                    urls = self.get_urls(domain)

                    for i,url in enumerate(urls): 
                        with requests.get(url, stream=True) as req:
                            
                            try:
                                total_size = int(req.headers['content-length'])
                                filename = domain.replace('.','_')+f'-{i}'+'warc.gz'
                                description = f'Downloading file {i+1}/{len(urls)}'
                                with open(filename, 'wb') as file:
                                    for chunk in tqdm.tqdm(req.iter_content(chunk_size=1024),desc=description,total=round(total_size/self.chunk_size)):
                                        if chunk:
                                            file.write(chunk)

                            except Exception as e:
                                print(f'Error: {e}')
                            
                
            else:
                print('ERROR: input not recognized.')
                

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #set short versions of commands
    def default(self, inp):
        if inp == 'q':
            return True

        if inp == 'lsd':
            self.do_list_domains(inp)

        if inp == 'dl':
            self.do_download(inp)

        if inp == 'd':
            self.do_domains(inp)

        if inp == 'ch':
            self.do_chunk(inp)

        if inp == '':
            print(inp)

if __name__ == '__main__':
    CC_Fetch().cmdloop()