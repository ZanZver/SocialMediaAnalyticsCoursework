from linkedin_api import Linkedin # API docs: https://linkedin-api.readthedocs.io
from creds import email, password # Credentials for login

def printGreeting():
    # LinkedinIn jobs analysis
    # By: Zan Zver
    text = """
██╗     ██╗███╗   ██╗██╗  ██╗███████╗██████╗ ██╗███╗   ██╗██╗███╗   ██╗         ██╗ ██████╗ ██████╗ ███████╗     █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗██╗███████╗
██║     ██║████╗  ██║██║ ██╔╝██╔════╝██╔══██╗██║████╗  ██║██║████╗  ██║         ██║██╔═══██╗██╔══██╗██╔════╝    ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝██╔════╝██║██╔════╝
██║     ██║██╔██╗ ██║█████╔╝ █████╗  ██║  ██║██║██╔██╗ ██║██║██╔██╗ ██║         ██║██║   ██║██████╔╝███████╗    ███████║██╔██╗ ██║███████║██║   ╚████╔╝ ███████╗██║███████╗
██║     ██║██║╚██╗██║██╔═██╗ ██╔══╝  ██║  ██║██║██║╚██╗██║██║██║╚██╗██║    ██   ██║██║   ██║██╔══██╗╚════██║    ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝  ╚════██║██║╚════██║
███████╗██║██║ ╚████║██║  ██╗███████╗██████╔╝██║██║ ╚████║██║██║ ╚████║    ╚█████╔╝╚██████╔╝██████╔╝███████║    ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████║██║███████║
╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝     ╚════╝  ╚═════╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚═╝╚══════╝
                                                                                                                                                                           
██████╗ ██╗   ██╗       ███████╗ █████╗ ███╗   ██╗    ███████╗██╗   ██╗███████╗██████╗                                                                                     
██╔══██╗╚██╗ ██╔╝██╗    ╚══███╔╝██╔══██╗████╗  ██║    ╚══███╔╝██║   ██║██╔════╝██╔══██╗                                                                                    
██████╔╝ ╚████╔╝ ╚═╝      ███╔╝ ███████║██╔██╗ ██║      ███╔╝ ██║   ██║█████╗  ██████╔╝                                                                                    
██╔══██╗  ╚██╔╝  ██╗     ███╔╝  ██╔══██║██║╚██╗██║     ███╔╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗                                                                                    
██████╔╝   ██║   ╚═╝    ███████╗██║  ██║██║ ╚████║    ███████╗ ╚████╔╝ ███████╗██║  ██║                                                                                    
╚═════╝    ╚═╝          ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝                                                                                                                                                                                                                                                                                                                            
    """
    print(text)

def createConnection():
    """ Create API connection with LinkedIn

    Returns:
        API_Connection (API): connection to LinkedIn
    """
    try:
        API_Connection = Linkedin(email, password)
        return API_Connection
    except exception as e:
        print(e)
        return None
    
def getJobs(api: Linkedin, filterDict: dict):
    """Get LinkedIn jobs based on the filter

    Args:
        api (connection): connection to LinkedIn, established in createConnection function
        filterDict (dict): dictionary that is used for filtering the jobs

    Returns:
        listed_jobs (dict): list of jobs (in JSON) that were found based on filterDict
        
    """
    listed_jobs = api.search_jobs(
                    keywords = filterDict["keywords"],\
                    companies = filterDict["companies"],\
                    experience = filterDict["experience"],\
                    job_type = filterDict["job_type"],\
                    job_title = filterDict["job_title"],\
                    industries = filterDict["industries"],\
                    location_name = filterDict["location_name"],\
                    remote = filterDict["remote"],\
                    listed_at = filterDict["listed_at"],\
                    distance = filterDict["distance"],\
                    limit = filterDict["limit"],\
                    offset = filterDict["offset"]
                )
    return listed_jobs

def connectNeo4J():
    pass

def insertIntoNeo4J():
    pass
    
def main():
    # Print greeting
    printGreeting()
    
    # Get API connection
    generated_API = createConnection()
    print(type(generated_API))

    # Get jobs based on filter
    job_filter = {
                    "keywords" : "BCU",\
                    "companies" : None,\
                    "experience" : None,\
                    "job_type" : None,\
                    "job_title" : None,\
                    "industries" : None,\
                    "location_name" : None,\
                    "remote" : False,\
                    "listed_at" : 86400,\
                    "distance" : None,\
                    "limit" : -1,\
                    "offset" : 0
                }
    print(type(job_filter))
    jobs = getJobs(generated_API, job_filter)
    print(jobs)


if __name__ == "__main__":
    main()