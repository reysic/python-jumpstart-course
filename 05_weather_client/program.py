import requests
import bs4
import collections

WeatherReport = collections.namedtuple('WeatherReport',
                                       'cond, temp, scale, loc')


def main():
    print_the_header()

    state = input('What US state do you want the weather for (e.g. OR)? ')
    city = input('What city in {} (e.g. Portland)? ')

    html = get_html_from_web(state, city)
    report = get_weather_from_html(html)

    print('The temp in {} is {}{} and {}'.format(
        report.loc,
        report.temp,
        report.scale,
        report.cond
    ))


def print_the_header():
    print('-----------------------------------')
    print('         WEATHER APP')
    print('-----------------------------------')
    print()


def get_html_from_web(state, city):
    url = 'http://www.wunderground.com/weather/us/{}/{}'.format(state.lower(), city.lower())
    response = requests.get(url)
    return response.text


def get_weather_from_html(html):
    # cityCss = 'h1'
    # weatherScaleCss = '.wu-unit-temperature .wu-label'
    # weatherTempCss = '.wu-unit-temperature .wu-value'
    # weatherConditionCss = '.condition-icon'

    soup = bs4.BeautifulSoup(html, 'html.parser')
    loc = soup.find('h1').get_text() \
        .replace(' Weather Conditions', '') \
        .replace('star_ratehome', '')
    condition = soup.find(class_='condition-icon').get_text()
    temp = soup.find(class_='wu-unit-temperature').find(class_='wu-value').get_text()
    scale = soup.find(class_='wu-unit-temperature').find(class_='wu-label').get_text()

    report = WeatherReport(cond=condition, temp=temp, scale=scale, loc=loc)
    return report


def cleanup_text(text: str):
    if not text:
        return text

    text = text.strip()
    return text


if __name__ == '__main__':
    main()
