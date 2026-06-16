from django.shortcuts import redirect

def redirect_back(
    request,
    default_url=None,
    back_url=None,
):
    target = (
        back_url
        or request.POST.get("next")
        or request.GET.get("next")
        or default_url
    )
    
    if not target:
        raise ValueError("Redirect target is required")

    return redirect(target)

def redirect_previous(
    request,
    default_url,
):
    return redirect(
        request.META.get("HTTP_REFERER", default_url)
    )


def smart_redirect(
    *,
    url_name=None,
    back_url=None,
    next_url=None,
):
    target = back_url or next_url or url_name

    if not target:
        raise ValueError("Redirect target is required")

    return redirect(target)