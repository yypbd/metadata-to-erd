import fire

from fire_command import FireCommand

if __name__ == '__main__':
    fire.Fire(FireCommand)

    # print(FireCommand().show_schemas())

    # puml = FireCommand().generate_erd(schema='public', use_table_comment=False, relation_type='laravel', out_filename='test.puml')
    # print(puml)

    # puml = FireCommand().generate_erd(schema='public', use_table_comment=False, relation_type='laravel')
    # print(puml)

    # puml = FireCommand().generate_erd(schema='yypbd', use_table_comment=False, relation_type='laravel')
    # print(puml)
