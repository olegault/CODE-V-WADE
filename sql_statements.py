
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
    FROM `policy`
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

# SQL statement to add main labels for a segment to the database.
catetgory_labels_insert = """
    INSERT INTO `category_label`
    (
        `segment_id`
        , `category_label`
    )
    VALUES (%s, %s)"""

# SQL statement to add attribute labels for a segment to the database.
attribute_labels_insert = """
    INSERT INTO `attribute_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to add attribute labels for a segment to the database.
attribute_variable_table_insert = """
    INSERT INTO `{table_name}`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""



# SQL statement to insert into individual category table
retention_period_label_insert = """
    INSERT INTO `retention_period_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
retention_purpose_label_insert = """
    INSERT INTO `retention_purpose_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
notification_type_label_insert = """
    INSERT INTO `notification_type_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
security_measure_label_insert = """
    INSERT INTO `security_measure_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
audience_type_label_insert = """
    INSERT INTO `audience_type_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""


# SQL statement to insert into individual category table
user_type_label_insert = """
    INSERT INTO `user_type_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
access_scope_label_insert = """
    INSERT INTO `access_scope_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
does_or_does_not_label_insert = """
    INSERT INTO `does_or_does_not_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
access_type_label_insert = """
    INSERT INTO `access_type_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""


# SQL statement to insert into individual category table
action_first_party_label_insert = """
    INSERT INTO `action_first_party_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
action_third_party_label_insert = """
    INSERT INTO `action_third_party_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
third_party_entity_label_insert = """
    INSERT INTO `third_party_entity_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
choice_scope_label_insert = """
    INSERT INTO `choice_scope_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
choice_type_label_insert = """
    INSERT INTO `choice_type_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
user_choice_label_insert = """
    INSERT INTO `user_choice_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
change_type_label_insert = """
    INSERT INTO `change_type_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
collection_mode_label_insert = """
    INSERT INTO `collection_mode_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
identifiability_label_insert = """
    INSERT INTO `identifiability_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
personal_information_type_label_insert = """
    INSERT INTO `personal_information_type_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
purpose_label_insert = """
    INSERT INTO `purpose_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""

# SQL statement to insert into individual category table
do_not_track_label_insert = """
    INSERT INTO `do_not_track_label`
    (
        `segment_id`
        , `attribute_label`
    )
    VALUES (%s, %s)"""