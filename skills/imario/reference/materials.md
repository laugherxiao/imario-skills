# The user's own material

## An image the user attached (creative test)

You can see the image but cannot pass its bytes. Respondents must see pixels, so never describe
the image in words and test the description.

1. Call `imario:request_upload` with the `audience_ids` and question you intend to use.
2. Read `if_upload_fails` before sending anything.
3. Send the file: run `curl_command` if you can run shell commands; otherwise the iMario card in
   the chat or `manual_upload_url` does it.
4. Pass the returned `ref` as `image_refs` to `imario:run_study`.

## A rough sketch of an idea

A description is legitimate here. Describe it in an `open_question` or `preference_test` with
`material_is_description=true`, and tell the user the test measured reactions to the description.

## A questionnaire or interview guide document

Transcribe its questions into `questions`, in order, and run it as `survey` or `guide`. Tell the
user that skip logic, grids and pictures inside questions did not carry over.
