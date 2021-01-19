import modules.appstore as appstore
import modules.command_line as command_line
import modules.actions as actions
import sys
import os


def get_access_token(args):
    try:
        access_token = appstore.create_access_token(
            issuer_id=args.issuer_id, key_id=args.key_id, key=args.key
        )
        return access_token
    except ValueError as error:
        sys.exit(error)


def get_app_id(args, access_token):
    if args.app_id == None:
        args.app_id = appstore.get_app_id(
            bundle_id=args.bundle_id, access_token=access_token
        )
    return args.app_id


def get_bundle_id(args, access_token):
    if args.bundle_id == None:
        args.bundle_id = appstore.get_bundle_id(
            app_id=args.app_id, access_token=access_token
        )
    return args.bundle_id


def list_categories(args):
    access_token = get_access_token(args)
    platforms = command_line.create_platform_filter_list(args)

    actions.list_categories(
        access_token=access_token,
        platforms=platforms,
        verbosity=args.verbosity,
    )


def list_apps(args):
    actions.list_apps(
        access_token=get_access_token(args),
        verbosity=args.verbosity,
    )


def list_versions(args):
    access_token = get_access_token(args)
    app_id = get_app_id(args, access_token)
    platforms = command_line.create_platform_filter_list(args)
    states = command_line.create_version_state_filter_list(args)

    actions.list_versions(
        access_token=access_token,
        app_id=app_id,
        platforms=platforms,
        states=states,
        verbosity=args.verbosity,
    )


def list_infos(args):
    access_token = get_access_token(args)
    app_id = get_app_id(args, access_token)
    states = command_line.create_version_state_filter_list(args)

    actions.list_infos(
        access_token=access_token,
        app_id=app_id,
        states=states,
        verbosity=args.verbosity,
    )


def list_screenshots(args):
    access_token = get_access_token(args)
    app_id = get_app_id(args, access_token)
    platforms = command_line.create_platform_filter_list(args)
    states = command_line.create_version_state_filter_list(args)

    actions.list_screenshots(
        access_token=access_token,
        app_id=app_id,
        platforms=platforms,
        states=states,
        version_limit=args.version_limit,
        verbosity=args.verbosity,
    )


def list_previews(args):
    access_token = get_access_token(args)
    app_id = get_app_id(args, access_token)
    platforms = command_line.create_platform_filter_list(args)
    states = command_line.create_version_state_filter_list(args)

    actions.list_previews(
        access_token=access_token,
        app_id=app_id,
        platforms=platforms,
        states=states,
        version_limit=args.version_limit,
    )


def download(args):
    access_token = get_access_token(args)
    app_id = get_app_id(args, access_token)
    bundle_id = get_bundle_id(args, access_token)

    version_states = (
        [args.version_state]
        if args.version_state is not None
        else list(appstore.VersionState)
    )
    actions.download(
        access_token=access_token,
        asset_dir=args.asset_dir,
        app_id=app_id,
        bundle_id=bundle_id,
        platforms=[args.platform],
        version_states=version_states,
        overwrite=args.overwrite,
    )


def publish(args):
    access_token = get_access_token(args)
    app_id = get_app_id(args, access_token)
    bundle_id = get_bundle_id(args, access_token)

    actions.publish(
        access_token=access_token,
        asset_dir=args.asset_dir,
        app_id=app_id,
        bundle_id=bundle_id,
        platform=args.platform,
        allow_create=not args.no_create_version,
        version_string=args.version_string or args.created_version_string,
        update_version_string=args.version_string is not None,
    )