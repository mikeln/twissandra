$(function(){

$('#spinner').hide();

// Submit post on submit
$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    inject_data();
});
//
// spinner
//
var counter = 0;
setInterval(funcion() {
    var frames=20;
    var frameWidth=32;
    var offset=counter * -frameWidth;
    document.getElementById("spinner").style.backgroundPosition=offset + "px" + " " + 0 + "px";
    counter++; if (counter>=frames) counter = 0;
}, 100);

//
// form inject_data posting
//
function inject_data() {
    console.log("inject data working") // sanity check
    console.log($('#id_numusers').val()+":"+$('#id_numtweets').val()+":"+$('#id_secdelay').val()+":"+$('#id_distroflag').val())

    var bSub = document.getElementById('inject-submit');
    bSub.disabled = true;
    var pStatus = document.getElementById('status');
    pStatus.innerHTML="Working";

    $('#spinner').show();
    

    $.ajax({
        //url: "inject_data/control/",
        url: "",
        type: "POST",
        data: { numusers : $('#id_numusers').val(),
            numtweets : $('#id_numtweets').val(),
            secdelay : $('#id_secdelay').val(),
            distroflag : $('#id_distroflag').val() },
        
        success : function(json) {
            $('#id_numusers').val('0');
            $('#id_numtweets').val('0');
            $('#id_secdelay').val('0');
            //$('#id_distroflag').val();
            console.log(json);
            console.log("success");

            pStatus.innerHTML="Finished";
        },

        error : function(xhr,errmsg,err) {
            $('#status').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                                            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console

            pStatus.innerHTML="Error";
        },

        complete : function(xhr,textStatus) {
            bSub.disabled = false;
            $('#spinner').hide();
        }

    });
};

//
// cross site scripting code...from https://gist.github.com/broinjc/db6e0ac214c355c887e5
// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
 
/*
The functions below will create a header with csrftoken
*/
 
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
 
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

});
