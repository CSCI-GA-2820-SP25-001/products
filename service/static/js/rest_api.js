$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#product_id").val(res.id);
        $("#product_name").val(res.name);
        $("#product_description").val(res.description);
        $("#product_price").val(res.price);
        $("#product_likes").val(res.likes);
        $("#like-btn").prop("disabled", false);
    }

    // Clears all form fields
    function clear_form_data() {
        $("#product_id").val("");
        $("#product_name").val("");
        $("#product_description").val("");
        $("#product_price").val("");
        $("#product_likes").val("");
        $("#like-btn").prop("disabled", true);
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty().append(message);
    }

    // ****************************************
    // Create a Product
    // ****************************************

    $("#create-btn").click(function () {
        let name        = $("#product_name").val();
        let description = $("#product_description").val();
        let price       = $("#product_price").val();
        let likes       = parseInt($("#product_likes").val()) || 0;

        let data = {
            name:        name,
            description: description,
            price:       price,
            likes:       likes
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type:        "POST",
            url:         "/products",
            contentType: "application/json",
            data:        JSON.stringify(data)
        });

        ajax.done(function(res) {
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res) {
            flash_message(res.responseJSON?.message || "Error creating product");
        });
    });

    // ****************************************
    // Update a Product
    // ****************************************

    $("#update-btn").click(function () {
        let product_id  = $("#product_id").val();
        let name        = $("#product_name").val();
        let description = $("#product_description").val();
        let price       = $("#product_price").val();
        let likes       = parseInt($("#product_likes").val()) || 0;

        let data = {
            name:        name,
            description: description,
            price:       price,
            likes:       likes
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type:        "PUT",
            url:         `/products/${product_id}`,
            contentType: "application/json",
            data:        JSON.stringify(data)
        });

        ajax.done(function(res) {
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res) {
            flash_message(res.responseJSON?.message || "Error updating product");
        });
    });

    // ****************************************
    // Retrieve a Product
    // ****************************************

    $("#retrieve-btn").click(function () {
        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type:        "GET",
            url:         `/products/${product_id}`,
            contentType: "application/json",
            data:        ""
        });

        ajax.done(function(res) {
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res) {
            clear_form_data();
            flash_message(res.responseJSON?.message || "Error retrieving product");
        });
    });

    // ****************************************
    // Delete a Product
    // ****************************************

    $("#delete-btn").click(function () {
        let product_id = $("#product_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type:        "DELETE",
            url:         `/products/${product_id}`,
            contentType: "application/json",
            data:        ""
        });

        ajax.done(function(res) {
            clear_form_data();
            flash_message("Product has been Deleted!");
        });

        ajax.fail(function(res) {
            flash_message(res.responseJSON?.message || "Error deleting product");
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        clear_form_data();
        $("#flash_message").empty();
    });

    // ****************************************
    // Search for a Product
    // ****************************************

    $("#search-btn").click(function () {
        // collect filters
        const params = {};
        const name        = $("#product_name").val();
        const description = $("#product_description").val();
        const price       = $("#product_price").val();

        if (name)        params.name        = name;
        if (description) params.description = description;
        if (price)       params.price       = price;

        // build querystring
        const qs = $.param(params);

        $("#flash_message").empty();

        let ajax = $.ajax({
            type:        "GET",
            url:         `/products${qs ? "?" + qs : ""}`,
            contentType: "application/json",
            data:        ""
        });

        ajax.done(function(res) {
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">';
            table += '<thead><tr>';
            table += '<th>ID</th><th>Name</th><th>Description</th><th>Price</th><th>Likes</th>';
            table += '</tr></thead><tbody>';

            let firstProduct = null;
            res.forEach((product, i) => {
                table += `<tr id="row_${i}">`
                      + `<td>${product.id}</td>`
                      + `<td>${product.name}</td>`
                      + `<td>${product.description}</td>`
                      + `<td>${product.price}</td>`
                      + `<td>${product.likes}</td>`
                      + `</tr>`;
                if (i === 0) firstProduct = product;
            });

            table += '</tbody></table>';
            $("#search_results").append(table);

            if (firstProduct) {
                update_form_data(firstProduct);
            }
            flash_message("Success");
        });

        ajax.fail(function(res) {
            flash_message(res.responseJSON?.message || "Error searching products");
        });
    });

    // ****************************************
    // Like a Product
    // ****************************************

    $("#like-btn").click(function () {
        const id = $("#product_id").val();
        if (!id) return;

        $("#flash_message").empty();

        let ajax = $.ajax({
            type:        "PUT",
            url:         `/products/${id}/like`,
            contentType: "application/json",
            data:        ""
        });

        ajax.done(function(res) {
            $("#product_likes").val(res.likes);
            flash_message("Product liked");
        });

        ajax.fail(function(res) {
            flash_message(res.responseJSON?.message || "Error liking product");
        });
    });

}); 