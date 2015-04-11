from kesh.schema.base import fields, KeshSchema, convert

post_history_type_id = {1: 'initial_title',
                        2: 'initial_body',
                        3: 'initial_tags',
                        4: 'edit_title',
                        5: 'edit_body',
                        6: 'edit_tags',
                        7: 'rollback_title',
                        8: 'rollback_body',
                        9: 'rollback_tags',
                        10: 'post_closed',
                        11: 'post_reopened',
                        12: 'post_deleted',
                        13: 'post_undeleted',
                        14: 'post_locked',
                        15: 'post_unlocked',
                        16: 'community_owned',
                        17: 'post_migrated',
                        18: 'question_merged',
                        19: 'question_protected',
                        20: 'question_unprotected',
                        21: 'post_disassociated',
                        22: 'question_unmerged',
                        24: 'suggested_edit_applied',
                        25: 'post_tweeted',
                        31: 'comment_discussion_moved_to_chat',
                        33: 'post_notice_added',
                        34: 'post_notice_removed',
                        35: 'post_migrated_away',
                        36: 'post_migrated_here',
                        37: 'post_merge_source',
                        38: 'post_merge_destiation'
                       }

post_close_reason = {1: 'exact_duplicate_old',
                     2: 'off_topic_old',
                     3: 'subjective_and_argumentative_old',
                     4: 'not_a_real_question_old',
                     7: 'too_localized_old',
                     10: 'general_reference_old',
                     20: 'noise_or_pointless_old',
                     101: 'duplicate',
                     102: 'off_topic',
                     103: 'unclear',
                     104: 'too_broad',
                     105: 'primarily_opinion_based'
                    }

post_history_schema_fields = {'Id': (fields.Integer, {'required':True}),
                             'PostHistoryTypeId': (fields.Integer, {'required':True}),
                             'PostId': (fields.Integer, {}),
                             'RevisionGUID': (fields.String, {}),
                             'CreationDate': (fields.DateTime, {}),
                             'UserId': (fields.Integer, {}),
                             'UserDisplayName': (fields.String, {}),
                             'Comment': (fields.String, {}),
                             'Text': (fields.String, {})
                             }
mixin = type('mixin', (), {name:func(attribute=convert(name), **args)
                           for name, (func, args) in post_history_schema_fields.items()})

class PostHistorySchema(KeshSchema, mixin):
    pass
@PostHistorySchema.preprocessor
def add_post_history_string(schema, input_data):
    try:
        input_data['post_history_type_string'] = post_history_type_id[input_data['post_history_type_id']]
    except KeyError:
        pass
    return input_data


if __name__ == '__main__':
    s = r'''{"Text" : "herp",
             "Comment" : "Derp",
             "Id" : "-1",
             "CreationDate" : "2008-07-31T00:00:00Z",
             "PostHistoryTypeId" : "10"
}'''

    schema = PostHistorySchema()

    data, errors = schema.loads(s)

    print(data, errors, sep='\n\n\n')
