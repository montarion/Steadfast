export interface Image {
    image_name: string
    author: string,
    operation_name: string,
    comments: string[],
    image_info: {
        path_to_file: string
    },
    id: number
}