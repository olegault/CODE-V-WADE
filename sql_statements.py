
# SQL statement to select Policy ID, App ID, and Policy URL from the raw policy table
select_cleaned_policies = """
    SELECT `id`
    FROM `run_41_raw_policy`
    WHERE `cleaned_html` IS NOT NULL
    AND `cleaned_html` != ''
"""
# SQL statement to check for an existing entry for a cleaned policy
select_classified_policy_ids = """
    SELECT DISTINCT(`policy_id`)
    FROM `run_41_segment`
"""

# SQL statement to get policy text for the current policy ID
select_policy_text = """
    SELECT `cleaned_text`, `cleaned_html`
    FROM `run_41_raw_policy`
    WHERE id = %s
"""

# SQL statement to add segment to the database.
segment_insert = """
    INSERT INTO `run_41_segment`
    (
        `policy_id`
        , `segment_text`
        , `main_category_label_first_party`
        , `main_category_label_third_party`
        , `identifiability_label_identifiable`
        , `identifiability_label_anonymized`
        , `identifiability_label_unspecified`
        , `purpose_label_additional_service`
        , `purpose_label_advertising`
        , `purpose_label_analytics`
        , `purpose_label_basic_service`
        , `purpose_label_legal`
        , `purpose_label_marketing`
        , `purpose_label_merger`
        , `purpose_label_personalization`
        , `purpose_label_service_operation`
        , `purpose_label_unspecified`
        , `information_type_computer_information`
        , `information_type_contact`
        , `information_type_cookies`
        , `information_type_demographic`
        , `information_type_financial`
        , `information_type_generic`
        , `information_type_health`
        , `information_type_ip_address`
        , `information_type_location`
        , `information_type_identifier`
        , `information_type_social`
        , `information_type_survey`
        , `information_type_activities`
        , `information_type_profile`
        , `information_type_unspecified`
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""