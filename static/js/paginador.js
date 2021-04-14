function removeParam(key, sourceURL) {
    var rtn = sourceURL.split("?")[0],
        param,
        params_arr = [],
        queryString = (sourceURL.indexOf("?") !== -1) ? sourceURL.split("?")[1] : "";
    if (queryString !== "") {
        params_arr = queryString.split("&");
        for (var i = params_arr.length - 1; i >= 0; i -= 1) {
            param = params_arr[i].split("=")[0];
            if (param === key) {
                params_arr.splice(i, 1);
            }
        }
        rtn = rtn + "?" + params_arr.join("&");
    }
    return rtn;
}

function cambiar_pagina(pagina) {
    url = window.location.href;
    url = url.replace("#", "");
    url = removeParam("page", url);
    url = removeParam("tab", url);
    url += ((url.substr(url.length-1,1) == "/") ? "?" : "&") + "page=" + pagina;

    try {
        if (ultimo_tab) {
            url += ((url.substr(url.length-1,1) == "/") ? "?" : "&") + "tab=" + ultimo_tab;
        }
    } catch (error) {
      console.error(error);
    }
    window.location.href = url;
}