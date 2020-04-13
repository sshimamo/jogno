import logging
import azure.functions as func
import mechanize

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    br = mechanize.Browser()
    br.set_handle_robots( False )
    br.open("https://relief.jogno.net/login")

    br.select_form(nr=0)
    br["email"] = req_body.get('email')
    br["password"] = req_body.get('password')
    br.submit()

    page = br.open("https://relief.jogno.net/newnotes/")

    rundate = req_body.get('year') + '-' + req_body.get('month') + '-' + req_body.get('day')
    newurl = page.geturl() + '?d=' + rundate
    br.open(newurl)
    br.select_form(nr=0)
    br["condition[weight]"] = req_body.get('weight') 
    br.submit()

    return func.HttpResponse(
        "This HTTP triggered function executed successfully.",
        status_code=200
    )