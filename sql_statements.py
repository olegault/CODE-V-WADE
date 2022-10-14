
# SQL statement to select Policy ID, App ID, and Policy URL from the raw policy table
# select_cleaned_policies = """
#     SELECT `id`
#     FROM `run_43_raw_policy`
#     WHERE `cleaned_html` IS NOT NULL
#     AND `id` NOT IN (SELECT policy_id FROM `run_43_all_classifier_results`)
#     AND `id` IN (SELECT policy_id FROM `app_to_policy`);
# """

# New SQL statement to select policies from `run_43_raw_policy` & `run_43_app_store_label` to check if small/empty
select_cleaned_policies = """
    SELECT DISTINCT `id`
    FROM `run_43_raw_policy`
    WHERE `id` IN (
        SELECT policy_id
        FROM
            `app_to_policy`
            JOIN `run_43_app_store_labels` ON `run_43_app_store_labels`.`app_id` = `app_to_policy`.`app_table_id`
    );
"""

# SQL statement to select Policy ID, segment ID App ID, and Policy URL from the raw policy table
select_classified_segments = """
    SELECT DISTINCT `segment_id`
    FROM `run_43_all_classifier_results`
"""

# SQL statement to select Policy ID, segment ID App ID, and Policy URL from the raw policy table
select_unclassified_segments = """
    SELECT `id`, `policy_id`
    FROM `run_43_segment`
    WHERE `id` NOT IN (SELECT `segment_id` from `run_43_all_classifier_results`)
"""

# SQL statement to check for an existing entry for a cleaned policy
select_classified_policy_ids = """
    SELECT DISTINCT(`policy_id`)
    FROM `run_43_all_classifier_results`
"""

# SQL statement to get policy text for the current policy ID
select_segment_text = """
    SELECT `segment_text`
    FROM `run_43_segment`
    WHERE id = %s
"""

# SQL statement to get policy text for the current policy ID
select_policy_text = """
    SELECT `cleaned_text`, `cleaned_html`
    FROM `run_43_raw_policy`
    WHERE id = %s
"""

# SQL statement to add segment to the database.
segment_insert = """
    INSERT INTO `run_43_segment`
    (
        `policy_id`
        , `segment_text`
        , `main_category_label_first_party`
        , `main_category_label_third_party`
        , `does_not_label`
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
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

large_segment_insert = """
    INSERT INTO `run_43_all_classifier_results` (
        `policy_id`,
        `segment_text`,
        `main_category_label_first_party`,
        `main_category_label_third_party`,
        `main_category_label_user_access_edit_deletion`,
        `main_category_label_data_retention`,
        `main_category_label_data_security`,
        `main_category_label_international_specific_audiences`,
        `main_category_label_do_not_track`,
        `main_category_label_policy_change`,
        `main_category_label_user_choice_control`,
        `main_category_label_introductory`,
        `main_category_label_practice_not_covered`,
        `main_category_label_privacy_contact_information`,
        `does_label`,
        `does_not_label`,
        `identifiability_label_identifiable`,
        `identifiability_label_anonymized`,
        `identifiability_label_unspecified`,
        `purpose_label_additional_service`,
        `purpose_label_advertising`,
        `purpose_label_analytics`,
        `purpose_label_basic_service`,
        `purpose_label_legal`,
        `purpose_label_marketing`,
        `purpose_label_merger`,
        `purpose_label_personalization`,
        `purpose_label_service_operation`,
        `purpose_label_unspecified`,
        `information_type_computer_information`,
        `information_type_contact`,
        `information_type_cookies`,
        `information_type_demographic`,
        `information_type_financial`,
        `information_type_generic`,
        `information_type_health`,
        `information_type_ip_address`,
        `information_type_location`,
        `information_type_identifier`,
        `information_type_social`,
        `information_type_survey`,
        `information_type_activities`,
        `information_type_profile`,
        `information_type_unspecified`,
        `retention_period_stated`,
        `retention_period_limited`,
        `retention_period_indefinitely`,
        `retention_period_unspecified`,
        `retention_purpose_advertising`,
        `retention_purpose_analytics`,
        `retention_purpose_legal`,
        `retention_purpose_marketing`,
        `retention_purpose_perform_service`,
        `retention_purpose_service_operation_security`,
        `retention_purpose_unspecified`,
        `notification_type_general_notice_on_privacy_policy`,
        `notification_type_general_notice_on_website`,
        `notification_type_no_notification`,
        `notification_type_personal_notice`,
        `notification_type_unspecified`,
        `security_measure_generic`,
        `security_measure_data_access_limitation`,
        `security_measure_privacy_review_audit`,
        `security_measure_privacy_training`,
        `security_measure_privacy_security_program`,
        `security_measure_secure_data_storage`,
        `security_measure_secure_data_transfer`,
        `security_measure_secure_user_authentication`,
        `security_measure_unspecified`,
        `audience_type_children`,
        `audience_type_calfornians`,
        `audience_type_citizens_from_other_countries`,
        `audience_type_europeans`,
        `user_type_with_account`,
        `user_type_without_account`,
        `user_type_unspecified`,
        `access_scope_profile_data`,
        `access_scope_transactional_data`,
        `access_scope_user_account_data`,
        `access_scope_other_data`,
        `access_scope_unspecified`,
        `access_type_deactivate_account`,
        `access_type_delete_account_full`,
        `access_type_delete_account_partial`,
        `access_type_edit_information`,
        `access_type_view`,
        `access_type_none`,
        `access_type_unspecified`,
        `action_first_party_collect_on_other_websites`,
        `action_first_party_collect_in_mobile_app`,
        `action_first_party_collect_on_mobile_website`,
        `action_first_party_collect_on_website`,
        `action_first_party_receive_from_other_parts_of_company`,
        `action_first_party_receive_from_other_service_named`,
        `action_first_party_receive_from_other_service_unnamed`,
        `action_first_party_track_on_other_websites`,
        `action_first_party_unspecified`,
        `action_third_party_collect_on_first_party`,
        `action_third_party_received_shared_with`,
        `action_third_party_see`,
        `action_third_party_track_on_first_party`,
        `action_third_party_unspecified`,
        `third_party_entity_named_third_party`,
        `third_party_entity_other_part_of_company`,
        `third_party_entity_other_users`,
        `third_party_entity_public`,
        `third_party_entity_unnamed_third_party`,
        `third_party_entity_unspecified`,
        `choice_scope_collection`,
        `choice_scope_first_party_collection`,
        `choice_scope_first_party_use`,
        `choice_scope_third_party_sharing_collection`,
        `choice_scope_third_party_use`,
        `choice_scope_both`,
        `choice_scope_use`,
        `choice_scope_unspecified`,
        `choice_type_browser_device_privacy_controls`,
        `choice_type_dont_use_service_feature`,
        `choice_type_first_party_privacy_controls`,
        `choice_type_opt_in`,
        `choice_type_opt_out_link`,
        `choice_type_opt_out_via_contacting_company`,
        `choice_type_third_party_privacy_controls`,
        `choice_type_unspecified`,
        `user_choice_none`,
        `user_choice_opt_in`,
        `user_choice_opt_out`,
        `user_choice_user_participation`,
        `user_choice_unspecified`,
        `change_type_merger`,
        `change_type_non_privacy_relevant`,
        `change_type_privacy_relevant`,
        `change_type_unspecified`,
        `collection_mode_explicit`,
        `collection_mode_implicit`,
        `collection_mode_unspecified`,
        `do_not_track_not_mentioned`,
        `do_not_track_honored`,
        `do_not_track_not_honored`,
        `do_not_track_mentioned_unclear_if_honored`,
        `do_not_track_other`
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""