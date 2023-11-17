# 1 rescue list of all US -> original bed V
# filter by size
# 2	rescue mininal sequence V
# 3 filter read with IF condition V
# 4 return data V

def intron(all_oneblock_read, genome_name, sd, sa, minimal_size, non_viral_genome):
	if non_viral_genome == None:
		if minimal_size == None:
			read_in_intron = 0
			other_genome_count = 0
			specific_genome_count = 0
			for read in all_oneblock_read:
				read = read.split("\t")
				genome = read[0]
				start = read[1]
				end = read[2]
				nb_block = read[9]
				if genome != genome_name:
					other_genome_count += 1
				else:
					specific_genome_count += 1
					if nb_block == "1":
						if int(start) > sd and int(start) < sa:
							read_in_intron += 1
						if int(end) > sd and int(end) < sa:
							read_in_intron += 1
						if int(end) > sa and int(start) < sd:
							read_in_intron += 1

			
			full_lenght = {"read_in_intron":read_in_intron, "other_genome_count":other_genome_count,\
						   "viral_genome_count":specific_genome_count,
						   "total_of_read":specific_genome_count+other_genome_count}
			return full_lenght

		else:
			read_in_intron = 0
			other_genome_count = 0
			specific_genome_count = 0
			for read in all_oneblock_read:
				read = read.split("\t")
				genome = read[0]
				start = read[1]
				end = read[2]
				nb_block = read[9]
				size = read[-2]; size = size.split(","); size = [int(x) for x in size]; size = sum(size)
				if size > minimal_size:
					if genome != genome_name:
						other_genome_count += 1
					else:
						specific_genome_count += 1
						if nb_block == "1":
							if int(start) > sd and int(start) < sa:
								read_in_intron += 1
							if int(end) > sd and int(end) < sa:
								read_in_intron += 1
							if int(end) > sa and int(start) < sd:
								read_in_intron += 1

			
			full_lenght = {"read_in_intron":read_in_intron, "other_genome_count":other_genome_count,\
						   "viral_genome_count":specific_genome_count,
						   "total_of_read":specific_genome_count+other_genome_count}
			
			return full_lenght

	else:
		if minimal_size == None:
			read_in_intron = 0
			other_genome_count = 0
			specific_genome_count = 0
			for read in all_oneblock_read:
				read = read.split("\t")
				genome = read[0]
				start = read[1]
				end = read[2]
				nb_block = read[9]
				if genome in non_viral_genome:
					other_genome_count += 1
				else:
					specific_genome_count += 1
					if genome == genome_name:
						if nb_block == "1":
							if int(start) > sd and int(start) < sa:
								read_in_intron += 1
							if int(end) > sd and int(end) < sa:
								read_in_intron += 1
							if int(end) > sa and int(start) < sd:
								read_in_intron += 1

			
			full_lenght = {"read_in_intron":read_in_intron, "other_genome_count":other_genome_count,\
						   "viral_genome_count":specific_genome_count,
						   "total_of_read":specific_genome_count+other_genome_count}
			return full_lenght

		else:
			read_in_intron = 0
			other_genome_count = 0
			specific_genome_count = 0
			for read in all_oneblock_read:
				read = read.split("\t")
				genome = read[0]
				start = read[1]
				end = read[2]
				nb_block = read[9]
				size = read[-2]; size = size.split(","); size = [int(x) for x in size]; size = sum(size)
				if size > minimal_size:
					if genome != genome_name:
						other_genome_count += 1
					else:
						specific_genome_count += 1
						if nb_block == "1":
							if int(start) > sd and int(start) < sa:
								read_in_intron += 1
							if int(end) > sd and int(end) < sa:
								read_in_intron += 1
							if int(end) > sa and int(start) < sd:
								read_in_intron += 1

			
			full_lenght = {"read_in_intron":read_in_intron, "other_genome_count":other_genome_count,\
						   "viral_genome_count":specific_genome_count,
						   "total_of_read":specific_genome_count+other_genome_count}
			
			return full_lenght


def main(all_oneblock_read, genome_name):
	sd = 144
	sa = 1299
	minimal_size = None
	non_viral_genome = None # must be a list
	data = intron(all_oneblock_read, genome_name, sd, sa, minimal_size, non_viral_genome)
	
	return data

if __name__ == '__main__':
	main()