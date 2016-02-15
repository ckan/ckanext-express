import pylons.config as config

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def editors_and_admins():
    '''Return the IDs of all group or organization editors and admins.

    Return a list of the user IDs of all users who are editors or admins of one
    or more groups or organizations.

    '''
    import ckan.model
    query = ckan.model.Session.query(ckan.model.Member)
    query = query.filter_by(table_name='user')
    query = query.filter(ckan.model.Member.capacity.in_(('editor', 'admin')))
    return list(set([member.table_id for member in query.all()]))


def sysadmins():
    '''Return a list of the user IDs of all the site's syadmin users.'''
    import ckan.model
    query = ckan.model.Session.query(ckan.model.User)
    query = query.filter_by(sysadmin=True)
    return [user.id for user in query.all()]


def _member_create(data_dict, result, max_editors):
    '''Don't allow more than max_editors to be created.

    An "editor" is defined as any user who is an editor or admin of any group
    or organization, or who is a sysadmin.

    Returns {'success': False} is the user is trying to create another
    "editor" and the site already has >= max_editors "editors".

    Otherwise, returns whatever the core member_create() auth function returns.

    If the core auth function returns {'success': False, 'msg': ...} this
    function will return that same dict - it will not override the core
    auth function's msg with its own.

    :param data_dict: the data dict that was posted to the member_create
                      action function
    :param result: the result dict from calling the core member_create auth
                   function with the request's data_dict and context
    :param max_editors: the maximum number of editors allowed
    :type max_editors: int

    '''
    # If the core auth function said no, we just say the same.
    if result['success'] is False:
        return result

    # If they are trying to create a normal membder (not an editor or admin),
    # always allow it.
    if data_dict.get('capacity') not in ('editor', 'admin'):
        return result

    # If the site has >= max_editors group or org editors or admins and
    # sysadmins, then don't allow another group or org editor or admin to be
    # created.
    editors_and_sysadmins = set(editors_and_admins() + sysadmins())
    if len(editors_and_sysadmins) >= max_editors:
        msg = toolkit._("You're only allowed to have {n} editors").format(
            n=max_editors)
        return {'success': False, 'msg': msg}

    # Otherwise, do allow one to be created.
    assert result['success'] is True
    return result


def _max_editors():
    '''Return the maximum number of editors allowed for this site (int).

    '''
    return toolkit.asint(config.get('ckan.express.max_editors', 3))


def member_create(context, data_dict):
    '''Custom member_create auth function.

    Does not allow more than max_editors "editors" (group/org editors/admins or
    sysadmins) to be created.

    max_editors is read from the config file.

    Otherwise defers to the core member_create auth function.

    '''
    import ckan.logic.auth.create

    result = ckan.logic.auth.create.member_create(context, data_dict)
    return _member_create(data_dict, result, _max_editors())


class UpToNEditorsPlugin(plugins.SingletonPlugin):
    '''A CKAN plugin that limits the site's number of "editors".

    An "editor" is any group/org editor or admin or a sysadmin.

    The allowed number of editors is read from the config file.

    '''
    plugins.implements(plugins.IAuthFunctions)

    def get_auth_functions(self):
        return {'member_create': member_create}

class ExpressPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    def update_config(self, config):
        toolkit.add_resource('fanstatic', 'ckanext-express')
