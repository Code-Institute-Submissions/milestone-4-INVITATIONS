const customiseInvite = {
    inviteFields: '',
    customScale: parseInt($(":root").css("--customizeScale")),
    divTemplateRaw: DIV_INPUT_TEMPLATE,
    customized_fields: [],

    hideFieldDetailDivs:(divNotToHide) => {
        // Hide all other field detail divs incase they were not closed.
        for (i in customiseInvite.inviteFields) {
            if (customiseInvite.inviteFields[i].name != divNotToHide) {
                $('#fields-' + customiseInvite.inviteFields[i].name).hide();
            }
        }
    },

    addFieldDiv:(fieldDetails) => {
        // Create field link and field div
        let fieldLink = document.createElement('a');
        fieldLink.id = `edit-${fieldDetails.name}`;
        fieldLink.title = `Edit '${customiseInvite.fieldDisplayName(fieldDetails.name)}'`;
        fieldLink.classList = 'edit__field custom__field';
        fieldLinkStyle = `top: ${(fieldDetails.y_pos / customiseInvite.customScale)}px;`;
        fieldLinkStyle += `height: ${((fieldDetails.raw_size / customiseInvite.customScale) * 1.5)}px;`;
        fieldLink.style = fieldLinkStyle;
        $('#design-preview').append(fieldLink);

        // Create div to show field contents on invite;
        let div = document.createElement('div');
        div.innerHTML = fieldDetails.text;
        div.classList = `field__${fieldDetails.name} custom__field`;
        div.id = `show-${fieldDetails.name}`;
        let divStyle = `font-family: ${fieldDetails.font};`;
        divStyle += `font-size: ${(fieldDetails.raw_size / customiseInvite.customScale)}px;`;
        divStyle += `color: ${fieldDetails.color};`;
        divStyle += `-webkit-text-stroke: ${fieldDetails.stroke_width} ${fieldDetails.stroke_fill};`;
        div.style = divStyle;
        $('#' + 'edit-' + fieldDetails.name).append(div);

        // Create event-listener for the field details div
        $('#show-' + fieldDetails.name).click(function(){
            customiseInvite.hideFieldDetailDivs(fieldDetails.name);
            $('#fields-' + fieldDetails.name).show();
        });
    },

    setFieldDivPosition:(fontSize, y_pos) => {
        // Set the divPosition based on the text y_pos, current font size,
        // the height of the invite and the height of the input div(120px)
        let defaultInputDivHeight = 120
        let divPosition = 120;
        if (customiseInvite.customScale == 4) {
            divPosition = ((y_pos / customiseInvite.customScale) + (fontSize * 1.5));
            inviteHeight = $('#design-preview').height();
            if ((divPosition + defaultInputDivHeight) > inviteHeight) {
                divPosition = (y_pos / customiseInvite.customScale) - defaultInputDivHeight;
            }
        }

        return divPosition;
    },

    addInputDiv:(fieldDetails) => {
        // Create div to hold all user input fields
        let div = document.createElement('div');
        div.classList = 'input__field';
        div.id = 'fields-' + fieldDetails.name;
        divPosition = customiseInvite.setFieldDivPosition((fieldDetails.raw_size / customiseInvite.customScale), fieldDetails.y_pos);
        divStyle = 'top: ' + divPosition + 'px;';
        div.style = divStyle;
        $('#design-preview').append(div);
    },

    fieldDisplayName:(fieldName) => {
        // Create field display name by replacing dash or underscore with a space
        // let str = fieldName.replace(/-|_/g, ' ').toLowerCase().substr(0, 11);
        // let words = str.split(' ');
        let words = fieldName.replace(/-|_/g, ' ').toLowerCase().substr(0, 11).split(' ');;
        let fieldTitle = words.map(word => {
            return word[0].toUpperCase() + word.substring(1);
        }).join(' ');
        return fieldTitle;
    },

    setFieldInputValues:(fieldDetails) => {
        $('#' + fieldDetails.name + '-text-color').val(fieldDetails.color);
        $('#' + fieldDetails.name + '-text-font').val(fieldDetails.font);
        resetSize = parseInt(fieldDetails.raw_size);
        $('#' + fieldDetails.name + '-text-size').val(resetSize);
        resetStrokeWidth = fieldDetails.stroke_width;
        $('#' + fieldDetails.name + '-stroke-width').val(resetStrokeWidth);
        $('#' + fieldDetails.name + '-stroke-color').val(fieldDetails.stroke_fill);
    },

    addFieldInputs:(fieldDetails) => {
        // Load in template string to create all inputs and swap in current values
        let divTemplate = customiseInvite.divTemplateRaw;
        divTemplate = divTemplate.replace(/{-invite-field-}/g, fieldDetails.name);
        divTemplate = divTemplate.replace(/{-field-name-}/g, customiseInvite.fieldDisplayName(fieldDetails.name));
        divTemplate = divTemplate.replace(/{-textContent-}/, fieldDetails.text);
        divTemplate = divTemplate.replace(/{-textColor-}/, fieldDetails.color);
        divTemplate = divTemplate.replace(/{-strokeColor-}/, fieldDetails.stroke_fill);

        // Set selected stroke width within the template string
        let strokeWidthLine = `<option value="${(fieldDetails.stroke_width)}">${(fieldDetails.stroke_width)}</option>`;
        let strokeWidthLineSelected = `<option value="${(fieldDetails.stroke_width)}" selected>${(fieldDetails.stroke_width)}</option>`;
        divTemplate = divTemplate.replace(strokeWidthLine, strokeWidthLineSelected);

        // Set selected font within the template string
        let pos2 = fieldDetails.font.indexOf("'", 2);
        let fontName = fieldDetails.font.substr(1, (pos2 - 1));
        let fontLine = `<option value="${fieldDetails.font}">${fontName}</option>`;
        let fontLineSelected = `<option value="${fieldDetails.font}" selected>${fontName}</option>`;
        divTemplate = divTemplate.replace(fontLine, fontLineSelected);

        // Set selected size within the template string
        fontOptionScaler = customiseInvite.customScale;
        if (customiseInvite.customScale == 6) { fontOptionScaler = customiseInvite.customScale / 1.5; }
        let sizeLine = `<option value="${fieldDetails.raw_size}">${(fieldDetails.raw_size / fontOptionScaler)}</option>`;
        let sizeLineSelected = `<option value="${fieldDetails.raw_size}" selected>${(fieldDetails.raw_size / fontOptionScaler)}</option>`;
        divTemplate = divTemplate.replace(sizeLine, sizeLineSelected);

        // Add inputs template to the InputDiv
        $('#fields-' + fieldDetails.name).append(divTemplate);

        // Create event-listener for the field divs buttons
        $('#btn-apply-' + fieldDetails.name).click(function(){
            customiseInvite.updateFieldDiv(fieldDetails);
        });
        $('#btn-cancel-' + fieldDetails.name).click(function(){
            $('#fields-' + fieldDetails.name).hide();
        });
        $('#btn-reset-' + fieldDetails.name).click(function(){
            customiseInvite.setFieldInputValues(fieldDetails);
        });

    },

    updateFieldDiv:(fieldDetails) => {
        // Update the div contents and styles to reflect the changes applied
        $('#fields-' + fieldDetails.name).hide();
        newText = $('#' + fieldDetails.name + '-text-content').val();
        if (newText == '') { newText = ' '; }
        newColor = $('#' + fieldDetails.name + '-text-color').val();
        newFont = $('#' + fieldDetails.name + '-text-font').val();
        newRawSize = $('#' + fieldDetails.name + '-text-size').val()
        newSize = `${newRawSize / customiseInvite.customScale}px`;
        testSize = Math.ceil($('#' + fieldDetails.name + '-text-size').val() / customiseInvite.customScale);
        newStrokeWidth = $('#' + fieldDetails.name + '-stroke-width').val();
        newStrokeColor = $('#' + fieldDetails.name + '-stroke-color').val();
        newStroke = newStrokeWidth + ' ' + newStrokeColor;
        $('#show-' + fieldDetails.name).text(newText);
        $('#show-' + fieldDetails.name).css('color', newColor);
        $('#show-' + fieldDetails.name).css('-webkit-text-stroke', newStroke);
        $('#show-' + fieldDetails.name).css('font-family', newFont);
        $('#show-' + fieldDetails.name).css('font-size', newSize);

        // Change the height of the dotted link box
        newLinkHeight = `${($('#' + fieldDetails.name + '-text-size').val() * 1.5) / customiseInvite.customScale}px`;
        $('#edit-' + fieldDetails.name).height(newLinkHeight);

        // Move the top position of the fieldDiv
        divPosition = customiseInvite.setFieldDivPosition(parseInt(newSize), fieldDetails.y_pos);
        let newTop = divPosition + 'px';
        $('#fields-' + fieldDetails.name).css('top', newTop);

        // Update customized fields
        newFieldDetails = {
            'name': fieldDetails.name,
            'text': newText,
            'y_pos': fieldDetails.y_pos,
            'font': newFont,
            'raw_size': newRawSize,
            'color': newColor,
            'stroke_fill': newStrokeColor,
            'stroke_width': newStrokeWidth,
        }
        replaceInviteLine = customiseInvite.customized_fields.findIndex((field) => field.name === fieldDetails.name);
        customiseInvite.customized_fields[replaceInviteLine] = newFieldDetails;

    },

    setupInviteActionButtons:() => {
        // Setup event listeners for invite action buttons
        $('#btn-invite-edit').click(function(){
            // Toggle the overlay which prevents invite edits and also the button icon
            $('#design-pause-overlay').toggle();
            if ($('#btn-invite-edit').html().includes('fa-ban')) {
                $('#btn-invite-edit').html('<i class="fas fa-edit"></i>');
                $('#btn-invite-edit').prop('title', 'Re-enable field editing.');
            } else {
                $('#btn-invite-edit').html('<i class="fas fa-ban"></i>');
                $('#btn-invite-edit').prop('title', 'Pause editing (helps pinch zoom on mobiles).');
            }
        });

        $('#btn-invite-reset').click(function(){
            // Reset all field values back to their defaults apart from text
            customiseInvite.inviteFields.map(inviteField => {
                customiseInvite.setFieldInputValues(inviteField);
                customiseInvite.updateFieldDiv(inviteField);
            });
        });

        $('#btn-customize-done').click(function(){
            // Completed customization pass the data back into the form field
            $(`#${DATA_RETURN_ID}`).val(JSON.stringify(customiseInvite.customized_fields));
            $("#customize-modal").modal('hide');
        });

    },

    setupInviteFields:() => {
        customiseInvite.inviteFields.forEach(inviteField => {
            customiseInvite.addFieldDiv(inviteField);
            customiseInvite.addInputDiv(inviteField);
            customiseInvite.addFieldInputs(inviteField);
        });
    },

    copyInviteFields:() => {
        customiseInvite.customized_fields = customiseInvite.inviteFields;
    }

}

// customiseInvite.setupInviteActionButtons();
// customiseInvite.copyInviteFields();
// customiseInvite.setupInviteFields();