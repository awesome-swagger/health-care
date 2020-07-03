export enum CapitalizationOptions {
	Uppercase,
	Capitalize,
	Lowercase
}

export const Capitalize = function (value: String, options: CapitalizationOptions = CapitalizationOptions.Capitalize): String {
	if(value === undefined || value === null || value.length <= 0)
		return value;
	
	if(value.length === 1 && options === CapitalizationOptions.Capitalize) {
		return value.toUpperCase();
	}

	switch(options) {
		case CapitalizationOptions.Uppercase:
			return value.toUpperCase();
		case CapitalizationOptions.Capitalize:
			return `${value[0].toUpperCase()}${value.substr(1)}`;
		case CapitalizationOptions.Lowercase:
			return value.toLowerCase();
		default:
			return value;
	}
}