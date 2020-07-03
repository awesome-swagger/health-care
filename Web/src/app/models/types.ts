export type errorFunc = (reason: string | Error) => void;
export type successFunc<T> = (data: T) => void;
export type StringIndexable<TValue> = { [index: string]: TValue }
export type NumberIndexable<TValue> = { [index: number]: TValue }
