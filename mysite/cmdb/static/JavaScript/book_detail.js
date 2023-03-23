<script>
    $("#send").click(function () {
        {#json数据#}
        var post_data={
            "name":"weihu",
        };

        $.ajax({
            url:"http://127.0.0.1:8000/ajax",
            type:"POST",
            {#发送json数据到服务器#}
            data:post_data,

            {#请求成功回调函数#}
            success:function (data) {
                alert(data)
                alert("请求成功")
            },
            {#请求失败回调函数#}
            error:function () {
                alert("服务器请求超时,请重试!")
            }

        });
    });
</script>