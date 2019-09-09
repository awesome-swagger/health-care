import { Observable } from "rxjs";

import { errorFunc } from "./models/types";
import { IHaveId } from "./models/ihaveid";

/**
 * Common utilities created to reduce duplicate code for consistent checks and methods.
 * NOTE: These do NOT work in the directly in HTML they need to be referenced from a controller property.
 */
export class Utils {
  private static readonly compareValues = {
    areEqual: 0,
    isGreaterThan: 1,
    isLessThan: -1,
  };

  /**
   * Compares 2 objects that implement the IHaveId interface. Returns true if they are equal based in the id, false otherwise
   * OR Compares 2 string values to determine if they are the equal (exact casing required)
   * @param item1 First object to be compared for equality
   * @param item2 Second object to be compared for equality
   */
  public static areEqual(item1: IHaveId | string, item2: IHaveId | string): boolean {
    if (Utils.isNullOrUndefined(item1) || Utils.isNullOrUndefined(item2)) {
      return false;
    }

    if (item1.hasOwnProperty('id') && item2.hasOwnProperty('id')) {
      return (item1 as IHaveId).id === (item2 as IHaveId).id;
    }

    return (item1 as string) === (item2 as string);
  }

  /**
   * convert an Observable call to a standard Promise
   * @param observable - Observable to convert to promise
   */
  public static convertObservableToPromise<T>(observable: Observable<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      const sub = observable.subscribe(
        (data: T) => resolve(data),
        (reason: string | Error) => this.standardErrorHandle(reject, reason),
        () => sub.unsubscribe()
      );
    });
  }

  /**
   * Compares 2 objects that implement the IHaveId interface. Returns true if they are equal based in the id, false otherwise
   * OR Compares 2 string values to determine if they are the equal (exact casing required)
   * @param item1 First object to be compared for equality
   * @param item2 Second object to be compared for equality
   * @param ascending A value indicating whether @item1 and @item2 should be reversed during comparison
   */
  public static compare(item1: IHaveId | string | number | Date, item2: IHaveId | string | number | Date, ascending: boolean = true): number {
    return this.compareBy(item1, item2, ascending, 'id');
  }

  /**
   * Compares 2 objects that contain the propery (id is default). Returns true if they are equal, false otherwise
   * OR Compares 2 string values to determine if they are the equal (exact casing required)
   * @param item1 First object to be compared for equality
   * @param item2 Second object to be compared for equality
   * @param ascending A value indicating whether @item1 and @item2 should be reversed during comparison
   * @param prop The property to be used for comparing the objects
   */
  public static compareBy<T>(item1: T, item2: T, ascending: boolean = true, prop?: string): number {
    const has1 = !Utils.isNullOrUndefined(item1);
    const has2 = !Utils.isNullOrUndefined(item2);

    if (!ascending) {
      const temp = item1;
      item1 = item2;
      item2 = temp;
    }

    if (!has1 && !has2) {
      return this.compareValues.areEqual;
    }

    if (has1 && !has2) {
      return this.compareValues.isGreaterThan;
    }

    if (!has1 && has2) {
      return this.compareValues.isLessThan;
    }

    if (!this.isNullOrWhitespace(prop) && item1.hasOwnProperty(prop) && item2.hasOwnProperty(prop)) {
      if (item1[prop] > item2[prop]) {
        return this.compareValues.isGreaterThan;
      }

      return item1[prop] < item2[prop]
        ? this.compareValues.isLessThan
        : this.compareValues.areEqual;
    }

    if (item1 > item2) {
      return this.compareValues.isGreaterThan;
    }

    return item1 < item2
      ? this.compareValues.isLessThan
      : this.compareValues.areEqual;
  }

  /**
   * Returns a value indicating whether the specified collection parameter is null/undefined, not an array or has no items in the collection.
   * @param collection - The collection to be validated
   * @returns { boolean }
   */
  public static isNullOrEmptyCollection<T>(collection: Array<T>): boolean {
    return this.isNullOrUndefined(collection) || Object.prototype.toString.call(collection) !== '[object Array]' || collection.length === 0;
  }

  /**
   * Returns a value indicating whether the specified object is null or undefined, false otherwise;
   * @param object - The object to be validated
   * @returns { boolean }
   */
  public static isNullOrUndefined<T>(object: T): boolean {
    return object === null || typeof object === 'undefined';
  }

  /**
   * Gets a value indicating whether the specified value is null/undefined or is equal to the true value
   * <string>"True", <string>"true", <boolean>true, <number>1, <string>"1" all return true, false otherwise.
   * @param input - The value to be processed
   * @returns { Boolean }
   */
  public static isNullOrTrueValue(input?: string | number | boolean) {
    return Utils.isNullOrUndefined(input) || Utils.isTrueValue(input);
  }

  /**
   * Returns a value indicating whether the specified input is a string and is not null or only white space characters.
   * @param input - the string input to be validated
   * @returns { boolean }
   */
  public static isNullOrWhitespace(input: string): boolean {
    return this.isNullOrUndefined(input) || typeof input !== 'string' || input.replace(/\s/g, '') === '';
  }

  /**
   * Gets a value indicating whether the specified value is NOT null/undefined and is equal to the true value
   * <boolean>true, <string>"True" || "true" || "T" || "t" || "1", <number>1 all return true, otherwise false.
   * @param input - The value to be processed
   * @returns { Boolean }
   */
  public static isTrueValue(input?: string | number | boolean) {
    var stringValue = (input || '').toString().toLowerCase().trim();

    return !Utils.isNullOrWhitespace(stringValue) && (
      input === true
      || stringValue === 'true'
      || stringValue === 't'
      || stringValue === '1'
    );
  }

  /**
   * Sort collection by specified property (id will be used by default)
   * @param collection Collection to be sorted
   * @param ascending A value indicating whether the collection should be sorted ascending
   * @param prop Property to be used for sorting collection
   */
  public static sort<T>(collection: Array<T>, ascending: boolean = true, prop?: string): Array<T> {
    if (this.isNullOrEmptyCollection(collection)) {
      return [];
    }

    prop = this.isNullOrWhitespace(prop)
      ? 'id'
      : prop;

    return collection.sort((obj1, obj2) => this.compareBy(obj1, obj2, ascending, prop));
  }

  private static standardErrorHandle(reject: errorFunc, reason: string | Error): void {
    console.error(reason);
    reject(reason);
  }
}
