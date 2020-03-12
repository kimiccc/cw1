import click
import requests
import urllib
import urllib.request
import urllib.parse

base_web='http://ml18y26c.pythonanywhere.com'

def post(session,action,data):
    url=base_web+action+'/'
    resp=session.post(url=url,json=data)
    return resp.json()

@click.group()
def client():
  pass

@click.command()
@click.option('--name', prompt='Username', help='Student Username.')
@click.option('--email', prompt='E-mail', help='Student Email.')
@click.option('--password', prompt='Password', help='Student Password.')
def register(name,email,password):
    dataa = {
        'name': name,
        'email': email,
        'password':password,
    }
    url = base_web+"/register/"
    response=requests.post(url=url,data=dataa)
    click.echo(response.json())


@click.command()
@click.option('--name', prompt='Username', help='Student Username.')
@click.option('--password', prompt='Password', help='Student Password.')
def login(name,password):
    dataa = {
        'name': name,
        'password':password,
    }
    # session= requests.Session()
    # # request=requests.request()
    url = base_web+"/login/"
    # response=requests.get(url=url,params=data)
    response=requests.post(url=url,data=dataa)
    # state = response.json().get('state')
    click.echo(response.json())


@click.command()
def logout():
    url = base_web+"/logout/"
    response=requests.get(url=url)
    click.echo(response.json())

@click.command()
def list():
    url = base_web+"/list/"
    response = urllib.request.urlopen(url)
    page_text = response.read()
    click.echo(page_text)

@click.command()
def view():
    url = base_web+"/view/"
    response = urllib.request.urlopen(url)
    page_text = response.read()
    click.echo(page_text)


@click.command()
@click.option('--professorid', prompt='Professor Id', help='Professor Id')
@click.option('--modulecode', prompt='Module Code', help='Module Code')
def average(professorid,modulecode):
    dataa = {
        'professorid': professorid,
        'modulecode':modulecode,
    }
    url = base_web+"/average/"
    response=requests.post(url=url,data=dataa)
    state=response.json().get('state')
    result = response.json().get('result')
    if(state=='success'):
        click.echo(result)
    else:
        click.echo(response.json())

@click.command()
@click.option('--professorid', prompt='Professor Id', help='Professor Id')
@click.option('--modulecode', prompt='Module Code', help='Module Code')
@click.option('--year', prompt='Year', help='Year')
@click.option('--semester', prompt='Semester', help='Semester')
@click.option('--rating', prompt='Rating(Please Input Number 1~5)', help='Rating')
def rate(professorid,modulecode,year,semester,rating):
    dataa = {
        'professorid': professorid,
        'modulecode': modulecode,
        'year': year,
        'semester': semester,
        'rating': rating,
    }
    url = base_web + "/rate/"
    response = requests.post(url=url, data=dataa)
    state = response.json().get('state')
    if (state == 'success'):
       pass
    else:
        click.echo(response.json())

client.add_command(register)
client.add_command(login)
client.add_command(logout)
client.add_command(list)
client.add_command(view)
client.add_command(average)
client.add_command(rate)

if __name__ == '__main__':
  client()

