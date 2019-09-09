export type errorFunc = (reason: string | Error) => void;
export type successFunc<T> = (data: T) => void;
