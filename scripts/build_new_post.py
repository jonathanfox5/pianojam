# ~/pyprojects/pianojam/scripts/venv/bin/python

import os


def main():

    # Get user input
    jam_no = int(input('Jam number: '))
    jam_year = int(input('Jam year (YYYY): '))
    jam_month = int(input('Jam month (MM): '))

    # Get paths to work with
    root_path = move_up_directory(os.path.realpath(__file__), 2)
    submission_path = os.path.join(root_path, 'submissions')
    posted_path = os.path.join(root_path, 'posted_jams')
    template_path = os.path.join(root_path, 'template.md')
    proposed_path = os.path.join(root_path, 'proposed_pieces.md')

    post_output_path = os.path.join(posted_path,
                               standard_file_format(jam_year, jam_month, jam_no, 'Posted'))

    jam_no_previous = jam_no - 1
    jam_year_previous, jam_month_previous = subtract_month(jam_year, jam_month)
    previous_submissions_path = os.path.join(submission_path,
                                             standard_file_format(jam_year_previous, jam_month_previous, jam_no_previous, 'Submissions'))

    # Check if there are previous submissions. If not, exit
    if not os.path.exists(previous_submissions_path):
        print('Could not find previous jam :' + previous_submissions_path)
        return

    # Read in data
    post_body = get_text_from_file(template_path)

    submissions = get_text_from_file(previous_submissions_path)

    jam_date_text = f'{month_no_to_text(jam_month)} {jam_year:04}'
    proposed_pieces = {'Classical': '', 'Jazz': '',
                       'Ragtime': '', 'Video Games': '', 'Anime': '', '3 month challenge': ''}
    for k in proposed_pieces.keys():
        proposed_pieces[k] = get_section_from_file(proposed_path, jam_date_text, k)

    # Replace placeholders in the template
    post_body = post_body.replace('<<[Submissions]>>', submissions)

    for k, v in proposed_pieces.items():
        post_body = post_body.replace(f'<<[{k}]>>', v)

    # Write to file
    write_text_to_new_file(post_output_path, post_body)

    # Print success
    print("Complete!")


def month_no_to_text(month_no):
    month_list = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']

    return month_list[month_no-1]


def get_section_from_file(file_path, first_header, second_header):
    file_object = open(file_path, 'rt')

    first_header_found = False
    second_header_found = False

    output = ''

    for line in file_object:

        # Extract data if we are in the right section, terminate on the next section header
        if second_header_found:
            if line.find('#') == 0:
                break
            output += line

        # Work out if we are in the right section yet
        if first_header_found:

            if line.find(second_header) >= 0:
                second_header_found = True

        elif line.find(first_header) >= 0:
            first_header_found = True

    file_object.close()

    return output


def write_text_to_new_file(file_path, file_text):
    file_object = open(file_path, 'w')
    file_object.write(file_text)
    file_object.close()


def get_text_from_file(file_path):
    file_object = open(file_path, 'rt')
    file_text = file_object.read()
    file_object.close()

    return file_text


def standard_file_format(jam_year, jam_month, jam_no, append_text):
    # e.g. 2018-05_Piano_Jam_#58_Submissions.md

    if len(append_text) > 0:
        append_text = '_' + append_text

    file_name = f'{jam_year:04}-{jam_month:02}_Piano_Jam_#{jam_no}{append_text}.md'

    return file_name


def subtract_month(jam_year, jam_month):
    jam_month -= 1

    if jam_month == 0:
        jam_month = 12
        jam_year -= 1

    return jam_year, jam_month


def move_up_directory(path, no_of_times):
    for i in range(no_of_times):
        path = os.path.dirname(path)

    return path


if __name__ == "__main__":
    main()
