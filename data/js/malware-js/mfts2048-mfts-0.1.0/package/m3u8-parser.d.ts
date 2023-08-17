declare module "m3u8-parser" {
    export interface Segment {
        duration: number;
        uri: string;
        key: {
            method: string;
            uri: string;
            iv?: {
                buffer: Buffer;
            };
        };
        timeline: number;
    }

    class Parser {
        manifest: {
            segments: Segment[]
        }
        push: Function
        end: Function
    }
}
