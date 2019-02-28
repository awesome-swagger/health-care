import { environment } from '../environments/environment';

export class AppConfig {

  public static baseUrl = environment.apiHost;
  public static apiUrl = AppConfig.createUrl('api');
  public static restAuthUrl = AppConfig.createUrl('rest-auth');
  public static authTokenUrl = AppConfig.createUrl('api-token-auth');
  public static resetPasswordUrl = AppConfig.createUrl('rest-auth/password/reset');

  public static createUrl(str: string): string {
    return `${this.baseUrl}/${str}/`;
  }

  public static createWithApiUrl(str: string): string {
    return `${this.baseUrl}/api/${str}/`;
  }
}
