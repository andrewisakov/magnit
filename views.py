#!/usr/bin/python3
import datetime
import os
import sys
import json
import urllib
import settings
import database


def _load_template(template, dataset):
    pass


def redirect(target='/view/'):
    status = '302 Found'
    return (status, target)


def delete_comment(request):
    # print('view.delete_comment:', request)
    request = request.split('=')
    database.delete_comment({'id': int(request[1])})
    return redirect('/view/')


def post_comment(post_data, template='comment.html'):
    post_data = {k: (int(v[0]) if k.endswith('_id') else v[0]) for k, v in urllib.parse.parse_qs(post_data.decode()).items()}
    # print('post_comment', post_data)
    database.insert_comment(post_data)
    return redirect('/view/')


def comment(template='comment.html'):
    # print(request_body)
    with open(os.path.join(settings.TEMPLATES, template)) as comment_form_html:
        html = '\n'.join(comment_form_html.readlines())
        # print('view.comment:', regions())
        html = html.replace('{% regions %}', regions())
        return None, html.encode()


def _village(village, template='village.html'):
    with open(os.path.join(settings.TEMPLATES, template)) as village_row_html:
        html = '\n'.join(village_row_html.readlines())
        # print(village)
        for v in village:
            html = html.replace('{% ' + str(v) + ' %}', str(village[v]))
        return html


def villages(request, template='villages.html'):
    region_id = int(json.loads(request)['id'])
    # print('villages.request', region_id)
    with open(os.path.join(settings.TEMPLATES, template)) as villages_html:
        html = '\n'.join(villages_html.readlines())
        rows = [_village(v) for v in database.get_villages(region_id)]
        html = html.replace('{% villages %}', '\n'.join(rows))
        # print('villages.html:', html)
        return None, html.encode()


def _region(region, template='region.html'):
    with open(os.path.join(settings.TEMPLATES, template)) as region_html:
        html = '\n'.join(region_html.readlines())
        # print(region)
        for r in region:
            html = html.replace('{% ' + r + ' %}', str(region[r]))
        return html


def regions(template='regions.html'):
    with open(os.path.join(settings.TEMPLATES, template)) as regions_html:
        html = '\n'.join(regions_html.readlines())
        rows = [_region(r) for r in database.get_regions()]
        # print('view.regions:', rows)
        html = html.replace('{% regions %}', '\n'.join(rows))
        return html


def _comment_row(comment, template='comment_row.html'):
    # print(comment)
    with open(os.path.join(settings.TEMPLATES, template)) as comment_row_html:
        html = '\n'.join(comment_row_html.readlines())
        for c in comment:
            # print(c, comment[c])
            html = html.replace('{% ' + c + ' %}', str(comment[c]))
        return html


def view(template='view.html'):
    # print('view.view:', settings.TEMPLATES, template)
    rows = [_comment_row(c) for c in database.get_comments()]
    with open(os.path.join(settings.TEMPLATES, template)) as tml:
        html = '\n'.join(tml.readlines())
        # print(html)
        return None, html.replace('{% comments %}', '\n'.join(rows)).encode()


def _stat_row(stat_row, template='stat_row.html'):
    with open(os.path.join(settings.TEMPLATES, template)) as tml:
        html = '\n'.join(tml.readlines())
        # print(html)
        for row in stat_row:
            html = html.replace('{% ' + row + ' %}', str(stat_row[row]))
        return html


def stat(template='view.html'):
    rows = [_stat_row(c) for c in database.get_stat()]
    # print('views.stat:', rows)
    with open(os.path.join(settings.TEMPLATES, template)) as tml:
        html = '\n'.join(tml.readlines())
        # print(html)
        return None, html.replace('{% comments %}', '\n'.join(rows)).encode()


def _stat_region_row(region_row, template='stat_region_row.html'):
    with open(os.path.join(settings.TEMPLATES, template)) as tml:
        html = '\n'.join(tml.readlines())
        for c, v in region_row.items():
            html = html.replace('{% ' + c + ' %}', str(v))
        return html


def stat_region(request, template='view.html'):
    request = request.split('=')
    rows = [_stat_region_row(c) for c in database.get_stat_region({request[0]: int(request[1])})]
    # print('view.stat_region:', rows)
    with open(os.path.join(settings.TEMPLATES, template)) as tml:
        html = '\n'.join(tml.readlines())
    return None, html.replace('{% comments %}', '\n'.join(rows)).encode()


if __name__ == '__main__':
    print(regions())
