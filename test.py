from fire_command import FireCommand


if __name__ == '__main__':
    # print(FireCommand().show_schemas())
    #

    # puml = FireCommand().generate_erd(schema='public', engine='puml', use_table_comment=False, relation_type='laravel', out_filename='test.puml')
    # print(puml)
    #
    # puml = FireCommand().generate_erd(schema='public', engine='puml', use_table_comment=False, relation_type='laravel')
    # print(puml)

    # puml = FireCommand().generate_erd(schema='yypbd', engine='puml', use_table_comment=False, relation_type='laravel', out_filename="samples/test.puml")
    # print(puml)

    d2 = FireCommand().generate_erd(schema='yypbd', engine='d2', use_table_comment=False, relation_type='laravel', out_filename="samples/test.d2")
    print(d2)
