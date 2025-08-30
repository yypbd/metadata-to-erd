from click.testing import CliRunner
from click_command import erd, schemas

if __name__ == '__main__':
    runner = CliRunner()

    # Test schemas command
    # result = runner.invoke(schemas)
    # print(result.output)

    # == postgres sample
    # result = runner.invoke(erd, [
    #     '--schema', 'public',
    #     '--engine', 'puml',
    #     '--use_table_comment', 'False',
    #     '--relation_type', 'laravel',
    #     '--out_filename', 'plantuml_sample.puml'
    # ])
    # print(result.output)

    # result = runner.invoke(erd, [
    #     '--schema', 'public',
    #     '--engine', 'puml',
    #     '--use_table_comment', 'False',
    #     '--relation_type', 'laravel'
    # ])
    # print(result.output)

    # == mysql sample
    # result = runner.invoke(erd, [
    #     '--schema', 'yypbd',
    #     '--engine', 'puml',
    #     '--use_table_comment', 'False',
    #     '--relation_type', 'laravel',
    #     '--out_filename', 'samples/plantuml_sample.puml'
    # ])
    # print(result.output)

    # Test erd command
    result = runner.invoke(erd, [
        '--schema', 'yypbd',
        '--engine', 'd2',
        '--use_table_comment', 'False',
        '--relation_type', 'laravel',
        '--out_filename', 'samples/d2_sample.d2'
    ])
    print(result.output)
