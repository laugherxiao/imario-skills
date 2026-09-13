# The user's own material

## An image the user attached (`image_reaction`)

You can see the image but cannot pass its bytes. Respondents must see pixels, so never describe
the image in words and test the description.

1. If the host supplies attachments as `image_files`, pass them straight to `imario:run_study`.
2. Otherwise call `imario:request_upload` and read `if_upload_fails` before sending anything.
3. Send the file: run `curl_command` if you can run shell commands and read the attachment;
   otherwise call `imario:request_manual_upload` for the iMario card, or give the user
   `manual_upload_url`.
4. Pass the returned `ref` as `image_refs` to `imario:run_study`, only after the upload reported
   `received: true`.

## A rough sketch of an idea

A description is legitimate here. Describe it in an `open_question` or `preference_test` with
`material_is_description=true`, and tell the user the study measured reactions to the description.

## A questionnaire or interview guide document

Transcribe its questions into `questions`, in order, and run it as `survey` or `guide`. Tell the
user that skip logic, grids and pictures inside questions did not carry over.
