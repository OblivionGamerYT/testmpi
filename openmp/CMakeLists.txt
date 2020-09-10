# file("openmp_check.c")

# file(GLOB INCLUDES "../include/*.h")

# add_library(voxel_lib ${SOURCES} ${INCLUDES})

# target_include_directories(voxel_lib PUBLIC ../include)

# add_compile_options(-Wall -Wextra -pedantic -Werror -fopenmp)

add_executable(openmp_check openmp_check.c)

find_package(OpenMP)
if(OpenMP_C_FOUND)
    target_link_libraries(openmp_check PUBLIC OpenMP::OpenMP_C)
endif()


# target_link_libraries(surf_voxel PRIVATE voxel_lib)
