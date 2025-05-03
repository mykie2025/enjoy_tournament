import { ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

// This is a simplified version of the cn utility function
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
