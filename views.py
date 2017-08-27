#!/usr/bin/python3
import datetime
import os
import sys
import json
import settings
import database


def _load_template(template, dataset):
    pass


def post_comment(post_data, template='comment.html'):
    print('post_comment', post_data)


def comment(request_body, template='comment.html'):
    print(request_body)
    with open(os.path.join(settings.TEMPLATES, template)) as comment_form_html:
        html = '\n'.join(comment_form_html.readlines())
        html = html.replace('{% regions %}', regions())
        return html.encode()


def _village(village, template='village.html'):
    with open(os.path.join(settings.TEMPLATES, template)) as village_row_html:
        html = '\n'.join(village_row_html.readlines())
        # print(village)
        for v in village:
            html = html.replace('{% ' + str(v) + ' %}', str(village[v]))
        return html


def villages(request, template='villages.html'):
    region_id = int(json.loads(request)['id'])
    print('villages.request', region_id)
    with open(os.path.join(settings.TEMPLATES, template)) as villages_html:
        html = '\n'.join(villages_html.readlines())
        rows = [_village(v) for v in database.get_villages(region_id)]
        html = html.replace('{% villages %}', '\n'.join(rows))
        print('villages.html:', html)
        return html.encode()


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
    rows = [_comment_row(c) for c in database.get_comments()]
    # if settings.APP_PATH
    with open(os.path.join(settings.TEMPLATES, template)) as tml:
        html = '\n'.join(tml.readlines())
        # print(html)
        return html.replace('{% comments %}', '\n'.join(rows))


def stat():
    pass


if __name__ == '__main__':
    print(regions())
