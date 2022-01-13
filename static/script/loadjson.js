$(document).ready(function(){
    $.getJSON('getjson/user',function(data){
        var userdata='';
        $.each(data,function(key,value){
            userdata+='<tr id='+value.account+'>';
            userdata+='<td>'+value.account+'</td>';
            userdata+='<td>'+value.password+'</td>';
            userdata+='<td>COMING SOON</td>';
            userdata+='</tr>';
        });
        $('#user_table').append(userdata);
    });
    $.getJSON('getjson/ticket',function(data){
        var userdata='';
        $.each(data,function(key,value){
            userdata+='<tr id='+value.account+'>';
            userdata+='<td>'+value.account+'</td>';
            userdata+='<td>'+value.name+'</td>';
            userdata+='<td>'+value.birthday+'</td>';
            userdata+='<td>'+value.cellphone+'</td>';
            userdata+='<td>'+value.choose_movie+'</td>';
            userdata+='<td>'+value.movie_type+'</td>';
            userdata+='<td>'+value.cinema+'</td>';
            userdata+='<td>'+value.session+'</td>';
            userdata+='<td>'+value.seat_row+'</td>';
            userdata+='<td>'+value.seat_num+'</td>';
            userdata+='<td>COMING SOON</td>';
            userdata+='</tr>';
        });
        $('#ticket_table').append(userdata);
    });
});